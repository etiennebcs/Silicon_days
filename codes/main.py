import csvManager

if __name__ == '__main__':
    # initialization
    csv = "../src/articles_fake.csv"
    columns_to_remove = ["text", "top_img", "authors", "movies", "images", "canonical_link", "meta_data"]
    feature_columns = ["nb_title_found", "date_gap", "url_rank", "src_rank"]

    # clean data
    csvManager.clean_data(csv, feature_columns)

    # insert feature_columns
    csvManager.insert_features_columns(csv, feature_columns)

    # insert target_column
    csvManager.insert_target_column(csv, "isFakeNews")

    # show data
    csvManager.show_data(csv)


