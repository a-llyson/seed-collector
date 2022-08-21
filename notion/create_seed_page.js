require('dotenv').config();

var MongoClient = require('mongodb').MongoClient;
var url = process.env.MONGO_DB;
const db_client = new MongoClient(url);

const { Client } = require('@notionhq/client');
const notion = new Client({ auth: process.env.NOTION_API_KEY });

const DB_NAME = "seed-storage"

const SEED_EMOJIS = {
    "Bean": "🎋",
    "Carrot": "🥕",
    "Cucumber": "🥒",
    "Eggplant": "🍆",
    "Fruit": "🍎",
    "Green": "🥬",
    "Herb": "🌿",
    "Strawberry": "🍓",
    "Tomato": "🍅",
    "Pea": "🟢",
    "Pepper": "🫑",
    "Pumpkin": "🎃",
};

const HERBS = ["anise", "basil", "bay leaf", "bergamot", "borage", "cumin", "cardamom", "catnip", "chervil", "chicory", "cilantro", "dill", "fennel", "ginger", "green onion", "horseradish", "lavender", "lemon balm", "lemon grass", "licorice", "lovage", "mint", "nutmeg", "oregano", "paprika", "parsley", "peppermint", "poppy seed", "rosemary", "saffron", "sage", "savory", "sesame", "sorrel", "tarragon", "thyme", "turmeric", "vanilla", "wasabi"];
const HERBS_LEN = HERBS.length;

const LEAFY_GREENS = ["artichoke", "arugula", "asian greens", "astro", "brocolli", "bok choi", "bok choy", "cabbage", "celery", "collard greens", "kale", "lettuce", "mustard greens", "pac choi", "pac choy", "rapini", "romaine", "spinach", "swiss chard", "watercress"];
const LEAFY_GREENS_LEN = LEAFY_GREENS.length;

// Returns list of collection names
async function get_collection_names() {
    var collection_names = []
    await db_client.connect().catch(err=>console.log(err));
    const db = db_client.db(DB_NAME);
    const collection_name_array = await db.listCollections().toArray();
    const length_array = collection_name_array.length;
    for (let i=0; i <length_array; i++) {
        collection_names[i] = collection_name_array[i]["name"];
    }
   // console.log(collection_names)
    return collection_names;
}

// Returns an array of seeds
async function get_collection_data(col_name) {
    await db_client.connect().catch(err=>console.log(err));
    const collection = db_client.db(DB_NAME).collection(col_name);
    const seed_array = await collection.find({}).toArray();
    return seed_array;
}
  

async function add_seed(emoji, name, price, quantity, select_type, url, store) {

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
            "rich_text": [
                {
                "type": "text",
                "text": {
                    "content": quantity
                }
            }
            ]
            
        },
        "Type": {
            "select": {
                "name": select_type
            }
        },
        "Link": {
            "url": url
        },
        "Store": {
            "select": {
                "name": store
            }
        },
    },
});
//   console.log(response);
};

 function get_emoji(seed) {
    const emoji_len = Object.keys(SEED_EMOJIS).length;
    seed = seed.toLowerCase();

    for (let i=0; i < emoji_len; i++) {
        seed_type = Object.entries(SEED_EMOJIS)[i][0];
        if (seed.includes(seed_type.toLowerCase())) {
            return [seed_type, SEED_EMOJIS[seed_type]];
        }
    }

    // Check if it's an herb
    for (let i=0; i < HERBS_LEN; i++) {
        if (seed.includes(HERBS[i])) {
            return ["Herb", "🌿"];
        }
    }

    // Check if it's a leafy green
    for (let i=0; i < LEAFY_GREENS_LEN; i++) {
        if (seed.includes(LEAFY_GREENS[i])) {
            return ["Green", "🥬"];
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
        data = data.concat(seeds); 
        
    }
    db_client.close();

    const total_seeds = data.length;
    for (let i=0; i<total_seeds; i++) {
        name = data[i]["seed"];
        emoji = get_emoji(name);

        price = data[i]["price"]
        if (typeof price == "string") {
            price = parseFloat(price);
        }

        quantity = data[i]["qty"]

        url = data[i]["url"];
        store = data[i]["store"];
        await add_seed(emoji[1], name, price, quantity, emoji[0], url, store);
    }

}
// add collection/website (where it comes from), make emoji[0] first letter uppercase,
// add more vegetable support,  do quantity/price,  

// for scrapers, save url to item object and maybe website name
// maybe for tags i should make the tag the website ??
query_db();