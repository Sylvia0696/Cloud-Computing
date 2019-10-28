import boto
from datetime import datetime
import pickle

MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''


def do_batch_write(items, table_name, dynamodb_table, dynamodb_conn):

    batch_list = dynamodb_conn.new_batch_write_list()
    batch_list.add_batch(dynamodb_table, puts=items)
    while True:
        response = dynamodb_conn.batch_write_item(batch_list)
        unprocessed = response.get('UnprocessedItems', None)
        if not unprocessed:
            break
        batch_list = dynamodb_conn.new_batch_write_list()
        unprocessed_list = unprocessed[table_name]
        items = []
        for u in unprocessed_list:
            item_attr = u['PutRequest']['Item']
            item = dynamodb_table.new_item(
                    attrs=item_attr
            )
            items.append(item)
        batch_list.add_batch(dynamodb_table, puts=items)


def import_csv_to_dynamodb(table_name, csv_file_name, colunm_names, column_types):
    '''
    Import a CSV file to a DynamoDB table
    '''        
    dynamodb_conn =     boto.connect_dynamodb(aws_access_key_id=MY_ACCESS_KEY_ID, aws_secret_access_key=MY_SECRET_ACCESS_KEY)
    dynamodb_table = dynamodb_conn.get_table(table_name)     
    BATCH_COUNT = 2 # 25 is the maximum batch size for Amazon DynamoDB

    items = []

    count = 0
    csv_file = open(csv_file_name, 'r',encoding='utf-8',newline='')
    for cur_line in reader(csv_file):
        count += 1

        row = {}
        for colunm_number, colunm_name in enumerate(colunm_names):
            row[colunm_name] = column_types[colunm_number]    (cur_line[colunm_number])
        row["insertedAtTimestamp"] = str(datetime.now())
        
        for key, value in row.copy().items():
            if value:
                continue
            else:
                row.pop(key, None)
        
        
        item = dynamodb_table.new_item(
                    attrs=row
            )           
        items.append(item)

        if count % BATCH_COUNT == 0:
            print ('batch write start ... ')
            do_batch_write(items, table_name, dynamodb_table, dynamodb_conn)
            items = []
            print ('batch done! (row number: ' + str(count) + ')')

    # flush remaining items, if any
    if len(items) > 0: 
        do_batch_write(items, table_name, dynamodb_table, dynamodb_conn)


    csv_file.close() 

def import_pickle_to_dynamodb(table_name, file_name, colunm_names):
    '''
    Import a CSV file to a DynamoDB table
    '''        
    dynamodb_conn = boto.connect_dynamodb(aws_access_key_id=MY_ACCESS_KEY_ID, aws_secret_access_key=MY_SECRET_ACCESS_KEY)
    dynamodb_table = dynamodb_conn.get_table(table_name)     
    BATCH_COUNT = 20 # 25 is the maximum batch size for Amazon DynamoDB

    items = []

    count = 0
    data = pickle.load(open(file_name, "rb" ))
    for i in data:
        count += 1

        row = {}
        row["id"] = i
        for colunm_number, colunm_name in enumerate(colunm_names):
            row[colunm_name] = str(data[i][colunm_name])
        
        row["insertedAtTimestamp"] = str(datetime.now())
        
        for key, value in row.copy().items():
            if value:
                continue
            else:
                row.pop(key, None)

        item = dynamodb_table.new_item(
                    attrs=row
            )           
        items.append(item)

        if count % BATCH_COUNT == 0:
            print ('batch write start ... ')
            do_batch_write(items, table_name, dynamodb_table, dynamodb_conn)
            items = []
            print ('batch done! (row number: ' + str(count) + ')')

    # flush remaining items, if any
    if len(items) > 0: 
        do_batch_write(items, table_name, dynamodb_table, dynamodb_conn)

def main():
    '''
    Demonstration of the use of import_pickle_to_dynamodb()
    We assume the existence of a table named `test_persons`, with
    - Last_name as primary hash key (type: string)
    - First_name as primary range key (type: string)
    '''
    colunm_names = 'alias name image_url rating category price location feature'.split()
    table_name = 'business'
    # csv_file_name = 'data.csv'
    pickle_name="business_new.pickle"
    import_pickle_to_dynamodb(table_name, pickle_name, colunm_names)


if __name__ == "__main__":
    main()
