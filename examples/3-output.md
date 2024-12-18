Sure! Let's create a simple React application using Convex to add and store notes. Below, I'll list the files needed and their respective code, as well as the necessary terminal commands for setting up and running the project.

### Terminal Commands

1. **Create the React app using Vite:**

   ```sh
   npm create vite@latest my-notes-app --template react
   ```

2. **Navigate into your React app directory:**

   ```sh
   cd my-notes-app
   ```

3. **Install Convex:**

   ```sh
   npm install convex
   npx convex dev
   ```

   This command will prompt you to set up your Convex project, authenticate, and will create the `convex/` directory with some initial scaffold files.

### Files and Code

1. **`index.tsx`** - Modify to wrap the app with `ConvexProvider`.

   ```jsx
   // src/main.tsx
   import React from "react";
   import ReactDOM from "react-dom/client";
   import { ConvexProvider, ConvexReactClient } from "convex/react";
   import App from "./App";
   import "./index.css";

   const convex = new ConvexReactClient(process.env.REACT_APP_CONVEX_URL);

   ReactDOM.createRoot(document.getElementById("root")!).render(
     <React.StrictMode>
       <ConvexProvider client={convex}>
         <App />
       </ConvexProvider>
     </React.StrictMode>
   );
   ```

2. **`convex/notes.ts`** - Define queries and mutations for notes.

   ```jsx
   // convex/notes.ts
   import { query, mutation } from "./_generated/server";
   import { v } from "convex/values";

   export const getAll = query({
     args: {},
     handler: async (ctx) => {
       return await ctx.db.query("notes").collect();
     },
   });

   export const add = mutation({
     args: { content: v.string() },
     returns: v.null(),
     handler: async (ctx, { content }) => {
       const note = { content };
       await ctx.db.insert("notes", note);
     },
   });
   ```

3. **Initialize Convex (Database Setup):**
   - Create a table by adding a schema to your Convex project. You can do this by creating a file like so:
   
   ```ts
   // convex/schema.ts

   import { defineSchema, defineTable, s } from "convex/schema";

   export default defineSchema({
     notes: defineTable({
       content: s.string(),
     }),
   });
   ```

   Save the file, then run the following to apply changes:
   
   ```sh
   npx convex push
   ```

4. **`App.tsx`** - Create a simple UI for adding and viewing notes.

   ```jsx
   // src/App.tsx
   import React, { useState } from "react";
   import { useQuery, useMutation } from "convex/react";
   import { api } from "../convex/_generated/api";

   function App() {
     const notes = useQuery(api.notes.getAll);
     const addNote = useMutation(api.notes.add);
     const [newNoteContent, setNewNoteContent] = useState("");

     const handleAddNote = async () => {
       await addNote({ content: newNoteContent });
       setNewNoteContent("");
     };

     return (
       <div>
         <h1>Notes</h1>
         <ul>
           {notes?.map((note, idx) => (
             <li key={idx}>{note.content}</li>
           ))}
         </ul>
         <input
           type="text"
           value={newNoteContent}
           onChange={(e) => setNewNoteContent(e.target.value)}
           placeholder="Add a new note"
         />
         <button onClick={handleAddNote}>Add Note</button>
       </div>
     );
   }

   export default App;
   ```

### Running the Application

After setting up the files, run:

```sh
npm run dev
```

This will start your Vite server, and you can access the Notes app in your browser. You can add notes using the input field and the "Add Note" button. Notes will be stored in your Convex database, and displayed in the list.

This example provides a good starting point for using Convex with React to manage data like notes. Feel free to expand and explore additional functionality and features!
