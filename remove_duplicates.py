def remove_duplicates(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        comments = f.readlines()

    unique_comments = list(set(comments))

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(unique_comments)

if __name__ == "__main__":
    input_file = "comments.txt"
    output_file = "unique_comments.txt"

    remove_duplicates(input_file, output_file)
