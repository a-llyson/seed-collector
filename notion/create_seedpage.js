require('dotenv').config();

var MongoClient = require('mongodb').MongoClient;
var url = process.env.MONGO_DB;
const db_client = new MongoClient(url);

const { Client } = require('@notionhq/client');
const notion = new Client({ auth: process.env.NOTION_API_KEY });

const db_name = "seed-storage"

// MongoClient.connect(url, function(err, client) {
//     const db = client.db(dbName)
//     db.listCollections().toArray(function(err, items) {
//         // gets names of all collections
//         for (let i = 0; i < items.length; i++) {
//             collection_names.push(items[i]["name"]);
//         }
//         client.close();
//    });
// })

// Returns list of collection names
async function get_collection_names() {
    collection_names = []
    await db_client.connect().catch(err=>console.log(err));
    const db = db_client.db(db_name);
    var collection_name_array = await db.listCollections().toArray();
    const length_array = collection_name_array.length
    for (let i=0; i <length_array; i++) {
        collection_names[i] = collection_name_array[i]["name"];
    }
    return collection_names;
}

// Returns an array of seeds
async function get_collection_data(col_name) {
    await db_client.connect().catch(err=>console.log(err));
    const collection = db_client.db(db_name).collection(col_name);
    const seed_array = await collection.find({}).toArray();
    return seed_array;
}

get_collection_names()  
    .then(console.log)
    .catch(console.error)
    .finally(() => dbClient.close());
get_collection_data("heritage")  
    .then(console.log)
    .catch(console.error)
    .finally(() => dbClient.close());
  
/*
(async () => {
  const response = await notion.pages.create({
    "cover": {
        "type": "external",
        "external": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
        }
    },
    "icon": {
        "type": "emoji",
        "emoji": "🥬"
    },
    "parent": {
        "type": "database_id",
        "database_id": process.env.NOTION_DATABASE_ID
    },
    "properties": {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": "Tuscan kale"
                    }
                }
            ]
        },
        "Description": {
            "rich_text": [
                {
                    "text": {
                        "content": "A dark green leafy vegetable"
                    }
                }
            ]
        },
        "Food group": {
            "select": {
                "name": "🥬 Vegetable"
            }
        }
    },
    "children": [
        {
            "object": "block",
            "heading_2": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Lacinato kale"
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "paragraph": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
                            "link": {
                                "url": "https://en.wikipedia.org/wiki/Lacinato_kale"
                            }
                        },
                        "href": "https://en.wikipedia.org/wiki/Lacinato_kale"
                    }
                ],
                "color": "default"
            }
        }
    ]
});
  console.log(response);
})();
*/