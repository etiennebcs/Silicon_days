import pandas as pd

pd.set_option('display.max_columns', None)  # show all columns of data


def clean_data(csv, columns_to_remove):
    try:
        # read csv_file
        data = pd.read_csv(csv)

        # check if data has these columns
        if set(columns_to_remove).issubset(data.columns):
            data_cleaned = data.drop(columns=columns_to_remove)

            # save data
            data_cleaned.to_csv(csv, index=False)
            print("Clearance completed\n")
            return True
        else:
            print("The csv_file has not such columns\n")
            return False

    except FileNotFoundError:
        print(f"File '{csv}' not found.\n")
        return False
    except Exception as e:
        print(f"Error occurred: {e}\n")
        return False


def insert_features_columns(csv, feature_columns):
    try:
        # read csv_file
        data = pd.read_csv(csv)

        for feature in feature_columns:
            # check if data has already these columns
            if feature not in data.columns:
                data[feature] = None

        # save data
        data.to_csv(csv, index=False)
        print("Insertion completed\n")

    except FileNotFoundError:
        print(f"File '{csv}' not found.\n")
        return False
    except Exception as e:
        print(f"Error occurred: {e}\n")
        return False


def insert_target_column(csv, target):
    try:
        # read csv_file
        data = pd.read_csv(csv)

        # check if data has already target columns
        if target not in data.columns:
            data[target] = None

            # save data
            data.to_csv(csv, index=False)
            print("Insertion completed\n")
        else:
            print("csv already has target column")
    except FileNotFoundError:
        print(f"File '{csv}' not found.\n")
        return False
    except Exception as e:
        print(f"Error occurred: {e}\n")
        return False


def show_data(csv):
    data = pd.read_csv(csv)
    print(data.iloc[1])
