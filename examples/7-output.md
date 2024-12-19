Here's how you can create a Convex-integrated React app that allows you to add and store notes. Below is the list of files you'll need to create, along with the necessary terminal commands to set up and run your application.

### File Structure
```
my-convex-notes-app/
├── convex/
│   ├── _generated/
│   └── notes.ts
├── src/
│   ├── components/
│   │   └── NotesApp.jsx
│   ├── App.jsx
│   ├── main.jsx
└── package.json
```

### Terminal Commands

1. **Create a new React project using Vite:**
   ```sh
   npm create vite@latest my-convex-notes-app --template react
   cd my-convex-notes-app
   ```

2. **Install Convex:**
   ```sh
   npm install convex
   ```

3. **Set up Convex (this will also prompt you to log in if necessary):**
   ```sh
   npx convex dev
   ```
   Note: Keep this command running as it’s needed to interact with the Convex backend locally.

### Files and Their Content

1. **`convex/notes.ts`**: This file will define the Convex queries and mutations for managing notes.
   ```typescript
   // convex/notes.ts
   import { query, mutation } from "./_generated/server";
   import { v } from "convex/values";

   export const getNotes = query({
     args: {},
     handler: async (ctx) => {
       return await ctx.db.query("notes").collect();
     },
   });

   export const addNote = mutation({
     args: {
       title: v.string(),
       content: v.string(),
     },
     handler: async (ctx, { title, content }) => {
       const note = { title, content, createdAt: new Date().toISOString() };
       await ctx.db.insert("notes", note);
     },
   });
   ```

2. **`src/components/NotesApp.jsx`**: This component handles the display and addition of notes.
   ```jsx
   // src/components/NotesApp.jsx
   import React, { useState } from 'react';
   import { useQuery, useMutation } from "convex/react";
   import { api } from "../../convex/_generated/api";

   function NotesApp() {
     const notes = useQuery(api.notes.getNotes);
     const addNote = useMutation(api.notes.addNote);

     const [title, setTitle] = useState('');
     const [content, setContent] = useState('');

     const handleAddNote = async () => {
       if (title && content) {
         await addNote({ title, content });
         setTitle('');
         setContent('');
       }
     };

     return (
       <div>
         <h1>Notes</h1>
         <input
           type="text"
           placeholder="Title"
           value={title}
           onChange={(e) => setTitle(e.target.value)}
         />
         <textarea
           placeholder="Content"
           value={content}
           onChange={(e) => setContent(e.target.value)}
         />
         <button onClick={handleAddNote}>Add Note</button>
         <ul>
           {notes?.map((note, index) => (
             <li key={index}>
               <h2>{note.title}</h2>
               <p>{note.content}</p>
             </li>
           ))}
         </ul>
       </div>
     );
   }

   export default NotesApp;
   ```

3. **`src/App.jsx`**: Simple wrapper to render the `NotesApp`.
   ```jsx
   // src/App.jsx
   import React from 'react';
   import NotesApp from './components/NotesApp';

   function App() {
     return (
       <div className="App">
         <NotesApp />
       </div>
     );
   }

   export default App;
   ```

4. **`src/main.jsx`**: Set up the Convex provider and render the app.
   ```jsx
   // src/main.jsx
   import React from 'react';
   import ReactDOM from 'react-dom';
   import App from './App';
   import { ConvexProvider, ConvexReactClient } from "convex/react";

   const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

   ReactDOM.createRoot(document.getElementById('root')).render(
     <React.StrictMode>
       <ConvexProvider client={convex}>
         <App />
       </ConvexProvider>
     </React.StrictMode>
   );
   ```

### How to Run

Once you have set up the files, run your application with:

```sh
npm run dev
```

Visit `http://localhost:5173` (or similar address given by Vite) to see your notes app in action, where you can add and store notes using the Convex backend.
