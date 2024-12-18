To create a Convex app that lets you add and store notes using a React frontend, follow these steps. Here’s the outline of the file structure and the necessary files:

### Terminal Commands

1. **Create a new Vite + React project:**
   ```sh
   npm create vite@latest my-notes-app --template react
   cd my-notes-app
   ```

2. **Install Convex:**
   ```sh
   npm install convex
   ```

3. **Initialize Convex:**
   ```sh
   npx convex dev
   ```

   Follow the prompts to finish setting up Convex for your project. This will create the `convex/` directory.

### Files and Code

1. **src/main.jsx**

   Modify the entry point to wrap your React app with the `ConvexProvider`.

   ```jsx
   import React from "react";
   import ReactDOM from "react-dom/client";
   import App from "./App";
   import { ConvexProvider, ConvexReactClient } from "convex/react";
   
   const convex = new ConvexReactClient(process.env.VITE_CONVEX_URL);
   
   ReactDOM.createRoot(document.getElementById('root')).render(
     <React.StrictMode>
       <ConvexProvider client={convex}>
         <App />
       </ConvexProvider>
     </React.StrictMode>
   );
   ```

2. **src/App.jsx**

   Create a basic component to display and add notes.

   ```jsx
   import React, { useState } from "react";
   import { useQuery, useMutation } from "convex/react";
   import { api } from "../convex/_generated/api";

   function App() {
     const notes = useQuery(api.notes.get);
     const addNote = useMutation(api.notes.add);
     
     const [noteText, setNoteText] = useState("");

     const handleAddNote = async () => {
       if (noteText.trim() === "") return;
       await addNote({ body: noteText });
       setNoteText("");
     };

     return (
       <div>
         <h1>Notes</h1>
         <input 
           type="text" 
           value={noteText} 
           onChange={(e) => setNoteText(e.target.value)} 
           placeholder="Write a new note"
         />
         <button onClick={handleAddNote}>Add Note</button>
         <ul>
           {notes && notes.map((note) => (
             <li key={note._id}>{note.body}</li>
           ))}
         </ul>
       </div>
     );
   }

   export default App;
   ```

3. **convex/notes.ts**

   Create this file within the `convex/` directory to define server-side logic for notes.

   ```typescript
   import { query, mutation } from "./_generated/server";
   import { v } from "convex/values";

   export const get = query({
     args: {},
     handler: async (ctx) => {
       return await ctx.db.query("notes").collect();
     },
   });

   export const add = mutation({
     args: { body: v.string() },
     returns: v.null(),
     handler: async (ctx, { body }) => {
       const note = { body };
       await ctx.db.insert("notes", note);
     },
   });
   ```

4. **Update convext project config:**

   After creating the `convex/notes.ts` file, you might need to ensure that the Convex CLI recognizes the newly created queries and mutations. If required, execute:

   ```sh
   npx convex codegen
   ```

This will generate the types and APIs needed for typesafe function calling.

5. **Setup environment variables**

   Ensure to set up your environment variable for `VITE_CONVEX_URL`, normally set via `.env` file or directly in `vite.config.js`.

   ```plaintext
   VITE_CONVEX_URL=<YOUR_CONVEX_URL_HERE>
   ```

Now you have a Convex app that lets you add and store notes!
