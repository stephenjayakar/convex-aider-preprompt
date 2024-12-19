Certainly! To create a basic shopping site with Convex and React, we will go through the necessary steps and files, focusing on shopping listings and cart functionality. Here's the outline:

### 1. Terminal Commands
1. Set up a new React project with Vite:
   ```sh
   npm create vite@latest shopping-site --template react
   cd shopping-site
   ```
2. Add Convex to the React app:
   ```sh
   npm install convex
   npx convex dev
   ```

### 2. Directory and File Structure
Here's a list of files and the code that needs to be written in each:

#### `src/main.jsx`
This is where we initialize our React application and wrap it with the `ConvexProvider`.

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { ConvexProvider, ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ConvexProvider client={convex}>
      <App />
    </ConvexProvider>
  </React.StrictMode>,
);
```

#### `src/App.jsx`
This is the main component of the app where we'll render the shopping list and the cart.

```jsx
import React from 'react';
import ItemList from './components/ItemList';

function App() {
  return (
    <div>
      <h1>Shopping Site</h1>
      <ItemList />
    </div>
  );
}

export default App;
```

#### `src/components/ItemList.jsx`
Displays items and allows adding them to the cart.

```jsx
import React, { useState } from 'react';
import { useQuery, useMutation } from 'convex/react';
import { api } from '../../convex/_generated/api';

function ItemList() {
  const items = useQuery(api.items.getItems);
  const addItemToCart = useMutation(api.items.addToCart);
  const purchaseItems = useMutation(api.items.purchaseItems);
  
  const [cart, setCart] = useState([]);

  const handleAddToCart = (item) => {
    if ((cart[item.id] || 0) < item.quantity) {
      setCart({
        ...cart,
        [item.id]: (cart[item.id] || 0) + 1,
      });
      addItemToCart({ itemId: item.id });
    }
  };

  const handlePurchase = () => {
    purchaseItems({ cart })
      .then(() => setCart({}));
  };

  if (!items) return <div>Loading...</div>;

  return (
    <div>
      <h2>Items</h2>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.name} - {item.price} - Available: {item.quantity}
            <button onClick={() => handleAddToCart(item)} disabled={(cart[item.id] || 0) >= item.quantity}>
              Add to Cart
            </button>
          </li>
        ))}
      </ul>

      <h2>Cart</h2>
      <ul>
        {Object.entries(cart).map(([itemId, quantity]) => {
          const item = items.find(i => i.id === itemId);
          return (
            <li key={itemId}>
              {item.name} - {quantity} x {item.price}
            </li>
          );
        })}
      </ul>
      <button onClick={handlePurchase}>
        Purchase
      </button>
    </div>
  );
}

export default ItemList;
```

#### `convex/items.ts`
This file holds the server-side code for querying the items, adding them to a cart, and purchasing logic.

```ts
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const getItems = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("items").collect();
  },
});

export const addToCart = mutation({
  args: { itemId: v.string() },
  handler: async (ctx, { itemId }) => {
    // In a real app, you might track the cart differently or use a session.
    // This function is a placeholder to simulate the action.
    return;
  },
});

export const purchaseItems = mutation({
  args: { cart: v.record(v.string(), v.number()) },
  handler: async (ctx, { cart }) => {
    for (const [itemId, quantity] of Object.entries(cart)) {
      const item = await ctx.db.getById("items", itemId);
      if (item && item.quantity >= quantity) {
        await ctx.db.patch(itemId, { quantity: item.quantity - quantity });
      }
    }
  },
});
```

#### `convex/schema.ts`
Define the schema for the `items` collection.

```ts
import { schema } from "convex/schema";

export default schema({
  items: {
    name: v.string(),
    price: v.float64(),
    quantity: v.int64(),
  },
});
```

### Set Up Steps

1. **Set up the database**: Populate the `items` collection with some initial data through the Convex console or a script.

By following the steps above, you would have set up a basic shopping site with item listings and cart functionality using React and Convex. Remember that each new tab will have its own local state for the cart, simulating separate users.
