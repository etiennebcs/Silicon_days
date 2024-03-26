import pandas as pd


class CSVHandler:
    def __init__(self, file):
        self.file = file

    def clean_data(self, col_to_delete):
        # read file
        data = pd.read_csv(self.file)

        # delete unecessary columns
        data_cleaned = data.drop(columns = col_to_delete)

        # save data
        data_cleaned.to_csv(self.file, index=False)
        print("Clearance completed")




# Utilisation de la classe CSVHandler
file = "dataset/articles_fake.csv"
col_to_delete = ["text", "top_img", "authors", "movies", "images", "canonical_link", "meta_data"]

handler = CSVHandler(file)
handler.clean_data(col_to_delete)
