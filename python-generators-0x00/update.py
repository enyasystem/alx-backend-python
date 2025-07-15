import csv
import uuid

input_file = "user_data.csv"
output_file = "user_data_with_id.csv"

with open(input_file, "r", newline='', encoding="utf-8") as infile, \
     open(output_file, "w", newline='', encoding="utf-8") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Read the original header and add 'user_id' at the front
    header = next(reader)
    writer.writerow(['user_id'] + header)


    # Use a set to track generated UUIDs and avoid duplicates
    generated_ids = set()
    for row in reader:
        # Generate a unique UUID
        while True:
            new_id = str(uuid.uuid4())
            if new_id not in generated_ids:
                generated_ids.add(new_id)
                break
        writer.writerow([new_id] + row)

print("Done! Check user_data_with_id.csv for the updated file.")
