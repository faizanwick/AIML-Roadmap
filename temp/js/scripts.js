(function () {
  "use strict";

  const TOKEN_STORAGE_KEY = "acess_token";
  const API_BASE = "http://127.0.0.1:8000";

  function authErrorMessage(payload, status) {
    const detail = payload && payload.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) {
      return detail.map(item => item.msg || JSON.stringify(item)).join("; ");
    }
    return status ? `Request failed (${status}).` : "Request failed.";
  }

  async function authRequest(path, body) {
    let response;
    try {
      response = await fetch(API_BASE + path, {
        method: "POST",
        headers: { Accept: "application/json", "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
    } catch (_) {
      throw new Error("Cannot reach the API. Make sure FastAPI is running on http://127.0.0.1:8000.");
    }
    let payload = null;
    try { payload = await response.json(); } catch (_) {}
    if (!response.ok) throw new Error(authErrorMessage(payload, response.status));
    return payload;
  }

  /* Login page */
  if (document.getElementById("login-form")) {
    const form = document.getElementById("login-form");
    const status = document.getElementById("auth-state");
    const submit = form.querySelector('[type="submit"]');

    if (new URLSearchParams(location.search).get("registered") === "1") {
      status.textContent = "Account created. Sign in to continue.";
      status.dataset.kind = "success";
    } else {
      status.textContent = "Enter your email and password to sign in.";
    }

    form.addEventListener("submit", async event => {
      event.preventDefault();
      submit.disabled = true;
      status.textContent = "Signing in…";
      status.dataset.kind = "loading";
      try {
        const result = await authRequest("/api/v1/auth/login", {
          email: document.getElementById("login-email").value.trim(),
          password: document.getElementById("login-password").value
        });
        if (!result || !result.access_token) throw new Error("No access token was returned.");
        localStorage.setItem(TOKEN_STORAGE_KEY, result.access_token);
        status.textContent = "Signed in. Opening your dashboard…";
        status.dataset.kind = "success";
        location.href = "/dashboard";
      } catch (error) {
        status.textContent = error.message;
        status.dataset.kind = "error";
      } finally {
        submit.disabled = false;
      }
    });
  }

  /* Register page */
  if (document.getElementById("register-form")) {
    const form = document.getElementById("register-form");
    const status = document.getElementById("auth-state");
    const submit = form.querySelector('[type="submit"]');
    status.textContent = "Create an account to start using TaskFlow.";

    form.addEventListener("submit", async event => {
      event.preventDefault();
      const password = document.getElementById("register-password").value;
      const confirm = document.getElementById("register-confirm").value;
      if (password !== confirm) {
        status.textContent = "Passwords do not match.";
        status.dataset.kind = "error";
        return;
      }
      submit.disabled = true;
      status.textContent = "Creating account…";
      status.dataset.kind = "loading";
      try {
        await authRequest("/api/v1/auth/register", {
          name: document.getElementById("register-name").value.trim(),
          email: document.getElementById("register-email").value.trim(),
          password
        });
        status.textContent = "Account created. Redirecting to login…";
        status.dataset.kind = "success";
        location.href = "/login";
      } catch (error) {
        status.textContent = error.message;
        status.dataset.kind = "error";
      } finally {
        submit.disabled = false;
      }
    });
  }

  /* Dashboard (dashboard.html) */
  if (document.getElementById("create-form")) {
    // Transport and endpoint paths remain isolated from dashboard presentation.
        const api = {
          base: API_BASE,
          async request(method, path, body) {
            const token = localStorage.getItem(TOKEN_STORAGE_KEY);
            const headers = { Accept: 'application/json' };
            if (body !== undefined) headers['Content-Type'] = 'application/json';
            if (token) headers.Authorization = 'Bearer ' + token;
            let response;
            try {
              response = await fetch(this.base.replace(/\/+$/, '') + path, {
                method,
                headers,
                ...(body === undefined ? {} : { body: JSON.stringify(body) })
              });
            } catch (_) {
              throw new Error('Cannot reach the API. Make sure FastAPI is running on http://127.0.0.1:8000.');
            }
            let payload;
            try { payload = await response.json(); } catch (_) { payload = null; }
            if (!response.ok) {
              const detail = payload?.detail;
              throw new Error(typeof detail === 'string' ? detail
                : Array.isArray(detail) ? detail.map(item => item.msg || JSON.stringify(item)).join('; ')
                : `Request failed (${response.status}).`);
            }
            return payload;
          },
          tasks() { return this.request('GET', '/api/v1/tasks/'); },
          task(id) { return this.request('GET', '/api/v1/tasks/task/' + encodeURIComponent(id)); },
          create(data) { return this.request('POST', '/api/v1/tasks/', data); },
          update(id, data) { return this.request('PUT', '/api/v1/tasks/'+ encodeURIComponent(id), data); },
          patch(id, data) { return this.request('PATCH', '/api/v1/tasks/'+ encodeURIComponent(id), data); },
          remove(id) { return this.request('DELETE', '/api/v1/tasks/' + encodeURIComponent(id)); },
          currentUser() { return this.request('GET', '/api/v1/auth/me');}
        };

        async function loadUserInfo() {
          const user = await api.currentUser();

          document.getElementById("user_id").textContent = 'User ID: { ' + user.user_id + ' }';
        }

        const $ = id => document.getElementById(id);
        const fields = ['title', 'description', 'priority', 'status', 'due_date', 'user_id'];
        const tabs = ['create', 'update', 'patch', 'delete', 'specific', 'all'];
        const taskId = task => task?.task_id ?? task?.id;
        const unwrapTask = value => value?.task ?? value;
        const listFrom = value => Array.isArray(value) ? value
          : Array.isArray(value?.tasks) ? value.tasks
          : Array.isArray(value?.items) ? value.items : [];
        let tasks = [];
        let selectedUpdate = null;
        let selectedDelete = null;
        let listLoaded = false;
        let loadSequence = 0;

        function state(tab, message, kind = 'empty') {
          const element = $(tab + '-state');
          element.textContent = message;
          element.dataset.kind = kind;
        }
        function activate(tab) {
          tabs.forEach(name => {
            const active = name === tab;
            $('panel-' + name).hidden = !active;
            $('tab-' + name).setAttribute('aria-selected', String(active));
            $('tab-' + name).tabIndex = active ? 0 : -1;
          });
        }
        document.querySelectorAll('[data-tab]').forEach(button => {
          button.addEventListener('click', () => activate(button.dataset.tab));
          button.addEventListener('keydown', event => {
            if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
            event.preventDefault();
            const current = tabs.indexOf(button.dataset.tab);
            const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1
              : (current + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
            activate(tabs[next]);
            $('tab-' + tabs[next]).focus();
          });
        });

        function values(form) {
          const result = {};
          fields.forEach(key => {
            const value = form.elements.namedItem(key).value.trim();
            result[key] = key === 'user_id' ? Number(value) : key === 'due_date' ? value || null : value;
          });
          return result;
        }
        function fillUpdate(task) {
          fields.forEach(key => {
            const input = $('update-form').elements.namedItem(key);
            input.value = key === 'due_date' ? String(task[key] || '').slice(0, 10)
              : task[key] ?? (key === 'priority' ? 'medium' : key === 'status' ? 'pending' : '');
          });
        }
        function renderDetails(element, task) {
          element.replaceChildren();
          if (!task || typeof task !== 'object') return;
          const keys = [...new Set(['task_id', 'title', 'description', 'priority', 'status', 'due_date', 'user_id', ...Object.keys(task)])];
          keys.forEach(key => {
            if (!(key in task) && !(key === 'task_id' && taskId(task) != null)) return;
            const group = document.createElement('div');
            const label = document.createElement('dt');
            const value = document.createElement('dd');
            label.textContent = key.replace(/_/g, ' ');
            const raw = key === 'task_id' ? taskId(task) : task[key];
            value.textContent = raw == null || raw === '' ? 'Not provided'
              : typeof raw === 'object' ? JSON.stringify(raw) : String(raw);
            group.append(label, value);
            element.append(group);
          });
        }
        function button(label, action, id) {
          const element = document.createElement('button');
          element.type = 'button';
          element.className = 'quiet';
          element.textContent = label;
          element.addEventListener('click', () => openFromList(action, id));
          return element;
        }
        function renderList() {
          if (!listLoaded) return;
          $('total-count').textContent = tasks.length;
          $('completed-count').textContent = tasks.filter(task => task.status === 'completed').length;
          $('pending-count').textContent = tasks.filter(task => task.status === 'pending').length;

          const options = document.createDocumentFragment();
          tasks.forEach(task => {
            if (taskId(task) == null) return;
            const option = document.createElement('option');
            option.value = String(taskId(task));
            option.label = String(task.title ?? '');
            options.append(option);
          });
          $('task-ids').replaceChildren(options);

          const query = $('search').value.trim().toLowerCase();
          const status = $('status-filter').value;
          const visible = tasks.filter(task =>
            (status === 'all' || task.status === status) &&
            `${task.title ?? ''} ${task.description ?? ''} ${taskId(task) ?? ''}`.toLowerCase().includes(query)
          );
          if ($('sort').value === 'title') {
            visible.sort((a, b) => String(a.title ?? '').localeCompare(String(b.title ?? '')));
          } else {
            const direction = $('sort').value === 'newest' ? -1 : 1;
            visible.sort((a, b) => direction * (
              (Date.parse(a.created_at ?? '') || Number(taskId(a)) || 0) -
              (Date.parse(b.created_at ?? '') || Number(taskId(b)) || 0)
            ));
          }
          const list = $('task-list');
          list.replaceChildren();
          visible.forEach(task => {
            const row = document.createElement('article');
            row.className = 'task-row';
            const info = document.createElement('div');
            info.className = 'min-w-0 flex-1';
            const title = document.createElement('h4');
            title.className = 'font-bold break-words';
            title.textContent = task.title || 'Untitled task';
            const description = document.createElement('p');
            description.className = 'muted mt-1 break-words';
            description.textContent = task.description || 'No description';
            const meta = document.createElement('div');
            meta.className = 'flex flex-wrap items-center gap-2 mt-3 text-sm muted';
            const badge = document.createElement('span');
            badge.className = 'status' + (task.status === 'completed' ? ' done' : '');
            badge.textContent = task.status || 'Unknown';
            const extra = document.createElement('span');
            extra.textContent = `#${taskId(task) ?? '—'} · ${task.priority || 'No priority'} · Due ${task.due_date || 'not set'}`;
            meta.append(badge, extra);
            info.append(title, description, meta);
            const actions = document.createElement('div');
            actions.className = 'flex flex-wrap gap-2';
            if (taskId(task) != null) {
              [['View', 'specific'], ['Update', 'update'], ['Patch', 'patch'], ['Delete', 'delete']]
                .forEach(([label, action]) => actions.append(button(label, action, taskId(task))));
            }
            row.append(info, actions);
            list.append(row);
          });
          state('all', !tasks.length ? 'No tasks yet. Create one to get started.'
            : !visible.length ? 'No tasks match your search or filters.'
            : `Showing ${visible.length} of ${tasks.length} tasks.`, visible.length ? 'success' : 'empty');
        }
        async function refreshTasks() {
          const sequence = ++loadSequence;
          const refreshButton = $('refresh-tasks');
          refreshButton.disabled = true;
          state('all', 'Loading tasks…', 'loading');
          try {
            const result = await api.tasks();
            if (sequence !== loadSequence) return;
            tasks = listFrom(result);
            listLoaded = true;
            renderList();
          } catch (error) {
            if (sequence !== loadSequence) return;
            listLoaded = false;
            state('all', error.message, 'error');
            $('task-list').replaceChildren();
            $('total-count').textContent = '—';
            $('completed-count').textContent = '—';
            $('pending-count').textContent = '—';
          } finally {
            if (sequence === loadSequence) refreshButton.disabled = false;
          }
        }
        function openFromList(tab, id) {
          activate(tab);
          if (tab === 'specific') { $('specific-id').value = id; $('specific-form').requestSubmit(); }
          if (tab === 'update') { $('update-id').value = id; $('update-load-form').requestSubmit(); }
          if (tab === 'delete') { $('delete-id').value = id; $('delete-load-form').requestSubmit(); }
          if (tab === 'patch') { $('patch-id').value = id; state('patch', 'Select only the fields you want to change.'); }
        }

        $('create-form').addEventListener('submit', async event => {
          event.preventDefault();
          const form = event.currentTarget;
          const submit = form.querySelector('[type="submit"]');
          submit.disabled = true;
          state('create', 'Creating task…', 'loading');
          try {
            await api.create(values(form));
            form.reset();
            state('create', 'Task created successfully.', 'success');
            await refreshTasks();
          } catch (error) { state('create', error.message, 'error'); }
          finally { submit.disabled = false; }
        });

        $('update-id').addEventListener('input', () => {
          selectedUpdate = null;
          $('update-form').hidden = true;
          state('update', 'Load this task to edit all its fields.');
        });
        $('update-load-form').addEventListener('submit', async event => {
          event.preventDefault();
          const id = $('update-id').value.trim();
          const submit = event.currentTarget.querySelector('[type="submit"]');
          selectedUpdate = null;
          $('update-form').hidden = true;
          submit.disabled = true;
          state('update', 'Loading task…', 'loading');
          try {
            const task = unwrapTask(await api.task(id));
            if ($('update-id').value.trim() !== id) return;
            if (!task || typeof task !== 'object') throw new Error('No task information was returned.');
            selectedUpdate = task;
            fillUpdate(task);
            $('update-form').hidden = false;
            state('update', 'Task loaded. Edit its fields and save.', 'success');
          } catch (error) { state('update', error.message, 'error'); }
          finally { submit.disabled = false; }
        });
        $('update-form').addEventListener('submit', async event => {
          event.preventDefault();
          if (!selectedUpdate || taskId(selectedUpdate) == null) {
            state('update', 'Load a task before saving.', 'error');
            return;
          }
          const submit = event.currentTarget.querySelector('[type="submit"]');
          submit.disabled = true;
          state('update', 'Saving changes…', 'loading');
          try {
            await api.update(taskId(selectedUpdate), values(event.currentTarget));
            state('update', 'Task updated successfully.', 'success');
            await refreshTasks();
          } catch (error) { state('update', error.message, 'error'); }
          finally { submit.disabled = false; }
        });

        $('patch-form').querySelectorAll('[data-field]').forEach(check => {
          check.addEventListener('change', () => {
            $('patch-form').elements.namedItem(check.dataset.field).disabled = !check.checked;
          });
        });
        $('patch-form').addEventListener('submit', async event => {
          event.preventDefault();
          const form = event.currentTarget;
          const id = $('patch-id').value.trim();
          const selected = [...form.querySelectorAll('[data-field]:checked')];
          if (!selected.length) { state('patch', 'Select at least one field to change.', 'error'); return; }
          const payload = {};
          for (const check of selected) {
            const key = check.dataset.field;
            const input = form.elements.namedItem(key);
            const value = input.value.trim();
            if (key === 'title' && !value) { state('patch', 'Enter a title for the selected title field.', 'error'); return; }
            if (key === 'user_id' && (!Number.isInteger(Number(value)) || Number(value) < 1)) {
              state('patch', 'Enter a valid user ID.', 'error'); return;
            }
            payload[key] = key === 'user_id' ? Number(value) : key === 'due_date' ? value || null : value;
          }
          const submit = form.querySelector('[type="submit"]');
          submit.disabled = true;
          state('patch', 'Applying patch…', 'loading');
          try {
            await api.patch(id, payload);
            state('patch', 'Selected fields updated successfully.', 'success');
            await refreshTasks();
          } catch (error) { state('patch', error.message, 'error'); }
          finally { submit.disabled = false; }
        });

        $('delete-id').addEventListener('input', () => {
          selectedDelete = null;
          $('delete-preview').hidden = true;
          $('delete-confirmation').hidden = true;
          state('delete', 'Load this task to review it before deleting.');
        });
        $('delete-load-form').addEventListener('submit', async event => {
          event.preventDefault();
          const id = $('delete-id').value.trim();
          const submit = event.currentTarget.querySelector('[type="submit"]');
          selectedDelete = null;
          $('delete-preview').hidden = true;
          $('delete-confirmation').hidden = true;
          submit.disabled = true;
          state('delete', 'Loading task…', 'loading');
          try {
            const task = unwrapTask(await api.task(id));
            if ($('delete-id').value.trim() !== id) return;
            if (!task || typeof task !== 'object') throw new Error('No task information was returned.');
            selectedDelete = { id, task };
            renderDetails($('delete-preview'), task);
            $('delete-preview').className = 'detail-grid max-w-3xl mb-5';
            $('delete-preview').hidden = false;
            $('delete-confirmation').hidden = false;
            state('delete', 'Review the task and confirm deletion.', 'success');
          } catch (error) { state('delete', error.message, 'error'); }
          finally { submit.disabled = false; }
        });
        $('delete-cancel').addEventListener('click', () => {
          $('delete-confirmation').hidden = true;
          state('delete', 'Deletion cancelled. The task was not changed.');
        });
        $('delete-confirm').addEventListener('click', async () => {
          if (!selectedDelete) { state('delete', 'Load a task before deleting.', 'error'); return; }
          const button = $('delete-confirm');
          button.disabled = true;
          state('delete', 'Deleting task…', 'loading');
          try {
            await api.remove(selectedDelete.id);
            selectedDelete = null;
            $('delete-preview').hidden = true;
            $('delete-confirmation').hidden = true;
            $('delete-id').value = '';
            state('delete', 'Task deleted successfully.', 'success');
            await refreshTasks();
          } catch (error) { state('delete', error.message, 'error'); }
          finally { button.disabled = false; }
        });

        $('specific-id').addEventListener('input', () => {
          $('specific-details').replaceChildren();
          state('specific', 'Enter a task ID to view its details.');
        });
        $('specific-form').addEventListener('submit', async event => {
          event.preventDefault();
          const id = $('specific-id').value.trim();
          const submit = event.currentTarget.querySelector('[type="submit"]');
          submit.disabled = true;
          $('specific-details').replaceChildren();
          state('specific', 'Loading task…', 'loading');
          try {
            const task = unwrapTask(await api.task(id));
            if ($('specific-id').value.trim() !== id) return;
            if (!task || typeof task !== 'object') throw new Error('No task information was returned.');
            renderDetails($('specific-details'), task);
            state('specific', 'Task details loaded.', 'success');
          } catch (error) { state('specific', error.message, 'error'); }
          finally { submit.disabled = false; }
        });

        $('refresh-tasks').addEventListener('click', refreshTasks);
        ['search', 'status-filter', 'sort'].forEach(id =>
          $(id).addEventListener(id === 'search' ? 'input' : 'change', renderList)
        );
        state('create', 'Complete the fields below to create a task.');
        state('update', 'Enter a task ID and load it to edit.');
        state('patch', 'Enter a task ID and select the fields to change.');
        state('delete', 'Enter a task ID to review it before deleting.');
        state('specific', 'Enter a task ID to view its details.');
        if (window.lucide) lucide.createIcons();
        refreshTasks();
        loadUserInfo();
  }
  
})();
