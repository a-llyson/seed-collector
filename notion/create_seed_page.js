require('dotenv').config();

var MongoClient = require('mongodb').MongoClient;
var url = process.env.MONGO_DB;
const db_client = new MongoClient(url);

const { Client } = require('@notionhq/client');
const notion = new Client({ auth: process.env.NOTION_API_KEY });

const db_name = "seed-storage"

const seed_emojis = {
    "green": "🥬",
    "tomato": "🍅",
    "cucumber": "🥒",
    "eggplant": "🍆",
    "herb": "🌿",
    "fruit": "🍎",
    "strawberry": "🍓",
    // "rest": "🌱",
}

// Returns list of collection names
async function get_collection_names() {
    var collection_names = []
    await db_client.connect().catch(err=>console.log(err));
    const db = db_client.db(db_name);
    const collection_name_array = await db.listCollections().toArray();
    const length_array = collection_name_array.length
    for (let i=0; i <length_array; i++) {
        collection_names[i] = collection_name_array[i]["name"];
    }
   // console.log(collection_names)
    return collection_names;
}

// Returns an array of seeds
async function get_collection_data(col_name) {
    await db_client.connect().catch(err=>console.log(err));
    const collection = db_client.db(db_name).collection(col_name);
    const seed_array = await collection.find({}).toArray();
    return seed_array;
}
  

async function add_seed(emoji, name, price, quantity, select_type) {
    console.log(emoji)
    console.log(name)
    console.log(price)
    console.log(quantity)
    console.log(select_type)
  const response = await notion.pages.create({
    "icon": {
        "type": "emoji",
        "emoji": emoji
    },
    "parent": {
        "type": "database_id",
        "database_id": process.env.NOTION_DATABASE_ID
    },
    "properties": {
        "Name": {
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": name
                    }
                }
            ]
        },
        "Price": {
            "number": price
        },
        "Quantity": {
            "number": quantity
        },
        "Type": {
            "select": {
                "name": select_type
            }
        }
    },
});
  console.log(response);
};

 function get_emoji(seed) {
    const emoji_len = Object.keys(seed_emojis).length
    seed = seed.toLowerCase();

    for (let i=0; i < emoji_len; i++) {
        seed_type = Object.entries(seed_emojis)[i][0];
        if (seed.includes(seed_type)) {
            return [seed_type, seed_emojis[seed_type]];
        }
    }
    return ["Other", "🌱"];
}


async function query_db() {
    const names = await get_collection_names()
        .catch(console.error);
    const names_len = names.length;
    var data = []
    for (let i=0; i<names_len; i++) {
        const seeds = await get_collection_data(names[i]).catch(console.error);
        // console.log(ans.length);
        data = data.concat(seeds); // adds ans to the data array
        
    }
    db_client.close();

    const total_seeds = data.length;
    for (let i=0; i<total_seeds; i++) {
        name = data[i]["seed"];
        emoji = get_emoji(name);
        // console.log(Object.entries(seed_emojis))
        // console.log(name.toLowerCase().includes(seed_emojis))
        // console.log(emoji[1])
        // console.log(name)
        // console.log(data[i]["price"])
        // console.log(data[i]["qty"])
        //console.log(emoji[0])
        price = data[i]["price"]
        if (typeof price == "string") {
            price = parseInt(price)
        }

        quantity = data[i]["qty"]
        if (typeof quantity == "string") {
            quantity = parseInt(quantity)
        }
        await add_seed(emoji[1], name, price, quantity, emoji[0]);
    }
    //console.log(Object.entries(seed_emojis)[0][0])
}

query_db();