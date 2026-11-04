total = 0
n = 0

try:
    with (
        open("data.txt", "r") as file,
        open("valid.txt", "w") as valid_file,
        open("invalid.txt", "w") as invalid_file
    ):
        for line in file:
            value = line.strip()

            try:
                number = float(value)
                total += number
                n += 1

                valid_file.write(value + "\n")

            except ValueError:
                print("Skipping invalid number:", value)
                invalid_file.write(value + "\n")

except FileNotFoundError:
    print("Input file not found.")

else:
    if n > 0:
        avg = total / n
        print("Average:", avg)

        with open("result.txt", "w") as file:
            file.write(str(avg))
    else:
        print("No valid records found.")