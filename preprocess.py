def convert_to_lowercase(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        unique_comments = f.readlines()

    lower_case_comments = [comment.lower() for comment in unique_comments]

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(lower_case_comments)

if __name__ == "__main__":
    input_file = "unique_comments.txt"
    output_file = "output_preprocess.txt"

    convert_to_lowercase(input_file, output_file)
