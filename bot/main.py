import pandas as pd


df = pd.read_excel('products.xlsx', sheet_name='Товары')
df1 = df[['Наименование', 'Категория', 'Цена, ₽']]


def get_data(category):
    product_list = []
    borders = df1['Категория'] == category
    for index, row in df1.loc[borders].iterrows():
        str1 = row['Наименование']
        """+ ' ' + \
            'Цена ' + str(int(row['Цена, ₽'])) + 'р'"""
        product_list.append(str1)
    return product_list
