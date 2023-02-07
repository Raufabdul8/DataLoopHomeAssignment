import dtlpy as dl
dl.login()

#Get an existing project
project = dl.projects.get(project_name="DemoProject")

#Q2.A
#Create a new dataset
dataset = project.datasets.create(dataset_name="pythonSdkDataSet2") 


#Q2.B
#Declare and upload labellist
label_list = ["class1", "class2", "key"] 
dataset.add_labels(label_list)

#Q2.C
#Upload Directory with 5 Images
dataset.items.upload(local_path="D:\DataLoopHomeAssignment\ImagesForUpload") 

#Get items
items_list = dataset.items.get_all_items() 

#Get item1
item_1 = items_list[0]

#Q2.D
#Update user metadata
import datetime
now = datetime.datetime.now().isoformat()
item_1.metadata["user"] = dict()
item_1.metadata["user"]["collected"] = now 
item_1.update()

#Q2.E Q2.F
#Add classification to images
for index, item in enumerate(items_list):
    label = 'class1' if index < 2 else 'class2'
    builder = item.annotations.builder()
    builder.add(annotation_definition=dl.Classification(label))
    item.annotations.upload(builder)

#Q2.G
#Add points to an item
import random
item_2 = items_list[1]
height = item_2.metadata['system']['height']
width = item_2.metadata['system']['width'] 
for counter in range(0,5):
    x = random.randint(0, width)
    y = random.randint(0, height)
    builder = item_2.annotations.builder()
    builder.add(annotation_definition=dl.Point(x, y, 'key'))
    item_2.annotations.upload(builder)


#Q3
#Query for items with class1 Label
filters = dl.Filters()
filters.add_join(field="label", values="class1")
pages = dataset.items.list(filters=filters)
for page in pages:
    for item in page:
        print({'name': item.name, 'id': item.id})

#Q4
#Query to get and print all point annotations
filters = dl.Filters()
filters.add_join(field='type', values='point')
pages = dataset.items.list(filters=filters)

items_list = []
for item in pages.all():     
    item_dict = {}
    item_dict['name'] = item.name
    item_dict['id'] = item.id
    item_dict['annotations'] = []
    for annotation in item.annotations.list():
            if(annotation.type == 'point'):
                    annotation_dict = {}
                    annotation_dict['id'] = annotation.id
                    annotation_dict['name'] = annotation.label
                    annotation_dict['x_value'] = annotation.x
                    annotation_dict['y_value'] = annotation.y
                    item_dict['annotations'].append(annotation_dict)
    items_list.append(item_dict)

print(items_list)


#Improvements Required

#Q2 - Improv
#Update user metadata
import datetime
now = datetime.datetime.now().isoformat()
filters = dl.Filters()
dataset.items.update(filters=filters, update_values={'collected': now})


#Q2.G - Improv
#Add points to an item
import random
item_2 = items_list[1]
height = item_2.metadata['system']['height']
width = item_2.metadata['system']['width'] 
builder = item_2.annotations.builder()
for counter in range(0,5):
    x = random.randint(0, width)
    y = random.randint(0, height)
    builder.add(annotation_definition=dl.Point(x, y, 'key'))
item_2.annotations.upload(builder)

#Q4
#Query to get and print all point annotations
filters = dl.Filters(resource=dl.FiltersResource.ANNOTATION)
filters.add(field='type', values='point')
pages = dataset.annotations.list(filters=filters)

items_dict = {}
for annotation in pages.all():   
    if annotation.item_id not in items_dict:
        items_dict[annotation.item_id] = []
    
    items_dict[annotation.item_id].append({
        'id': annotation.id,
        'name': annotation.label,
        'x_value': annotation.x,
        'y_value': annotation.y
    })


print(items_dict)

