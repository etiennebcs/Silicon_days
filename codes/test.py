import pandas as pd
import csvManager
import targetManager
import featureManager

import re

from codes import urlManager

if __name__ == '__main__':
    # initialization
    csv = "../src/articles.csv"
    columns_to_remove = ["url_rank", "src_rank"]
    feature_columns = ["nb_title_found", "url_rank", "src_rank"]

    # clean data
    #csvManager.clean_data(csv, columns_to_remove)
    """
    data = pd.read_csv(csv)
    cols_with_missing = [col for col in data.columns if data[col].isnull().any()]
    missing_val_count_by_column = (data.isnull().sum())
    print(cols_with_missing)
    print(missing_val_count_by_column)
    """

    # insert feature_columns
    #csvManager.insert_features_columns(csv, feature_columns)

    # insert target_column
    #csvManager.insert_target_column(csv, "isFakeNews")




    """
             data = pd.read_csv(csv)
    for index, row in data.iterrows():
        date = str(row['publish_date'])

        print(date)
        
            if (index <=95 ):
            val = row["nb_title_found"]
            print(f"nb = {val}")

            if (val >= 1000000):
                data.at[index, 'nb_title_found'] = 0.0

    """

    #data.to_csv(csv, index=False)


    # show data
    #csvManager.show_data(csv)

    # merge data
    #csvManager.concat_2csv("src/articles.csv", "src/P_real.csv", 1000, "src/articles.csv")

    url1 = 'https://www.lemonde.fr/international/article/2024/03/26/attentat-du-crocus-city-hall-apres-avoir-accuse-kiev-moscou-designe-les-occidentaux_6224318_3210.html'

    L = urlManager.extract_news_data(url1)
    print(L)
