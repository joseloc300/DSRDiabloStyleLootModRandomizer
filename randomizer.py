import csv
import random
import os

npcParamHeader = []
npcParamRows = []
npcParamItemLodColumnIndexes = []

rowIndexesToRandomize = []

randomizedNpcParamRows = []

def print_help():
    return

def read_csv():
    with open('./originalCSVs/NpcParam.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            print(', '.join(row))

            if len(npcParamItemLodColumnIndexes) == 0:
                npcParamHeader.extend(row)
                index = 0
                while len(row) > 0:
                    if (row[0].startswith("itemLotId_")):
                        npcParamItemLodColumnIndexes.append(index)
                    index+=1
                    row.pop(0)
            else:
                npcParamRows.append(row)

def collect_all_npc_item_lot_ids():
    itemLotIds = []

    rowIndex = -1
    for parsedRow in npcParamRows:
        rowIndex += 1
        hasAllItemLotIds = True
        currRowItemLotIds = []
        for itemLotIndex in npcParamItemLodColumnIndexes:
            if itemLotIndex >= len(parsedRow) or parsedRow[itemLotIndex] == '-1':
                hasAllItemLotIds = False
                break
            currRowItemLotIds.append(parsedRow[itemLotIndex])
        
        if not hasAllItemLotIds:
            continue

        rowIndexesToRandomize.append(rowIndex)
        itemLotIds.extend(currRowItemLotIds)

    return itemLotIds

def randomize_data():
    randomize_table_assignment()

def randomize_table_assignment():
    random.seed()
    itemLotIds = collect_all_npc_item_lot_ids()

    rowIndex = -1
    for paramRow in npcParamRows:
        rowIndex+=1
        if rowIndexesToRandomize.count(rowIndex) == 0:
            randomizedNpcParamRows.append(paramRow)
            continue

        for itemLotColumnIndex in npcParamItemLodColumnIndexes:
            randItemLotIdIndex = random.randint(0, len(itemLotIds)-1)
            randItemLotId = itemLotIds[randItemLotIdIndex]
            paramRow[itemLotColumnIndex] = randItemLotId

            itemLotIds.pop(randItemLotIdIndex)

        randomizedNpcParamRows.append(paramRow)

    if len(itemLotIds) > 0:
        print("leftover itemLotIds. " + str(len(itemLotIds)) + " were found. Something went wrong during the process.")

    return

def randomize_table_contents_all():
    print("TODO")
    return

def randomize_table_contents_same_cat():
    print("TODO")
    return

def randomize_item_sp_effects():
    print("TODO")
    return

def write_output():
    outputPath = "./randomizedCSVs/"
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    with open(outputPath + '/NpcParam.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(npcParamHeader)
        for randomizedRow in randomizedNpcParamRows:
            writer.writerow(randomizedRow)

def main():
    read_csv()
    randomize_data()
    write_output()
    return


main()