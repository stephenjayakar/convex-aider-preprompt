To create a Convex app that lets you add and store notes using React, I'll guide you through the necessary steps, files, and code snippets. Here's an outline of what we'll need:

### Terminal Commands:

1. **Set Up a React App (if needed):**
   ```sh
   npx create-react-app convex-notes-app
   cd convex-notes-app
   ```

2. **Install Convex:**
   ```sh
   npm install convex
   npx convex dev
   ```

### File Structure and Code:

1. **Setup Convex Client in React:**

   Create or modify `index.js` or `index.tsx` (depending on your setup):
   ```jsx
   import React from 'react';
   import ReactDOM from 'react-dom';
   import './index.css';
   import App from './App';
   import { ConvexProvider, ConvexReactClient } from 'convex/react';

   const convex = new ConvexReactClient(process.env.REACT_APP_CONVEX_URL);

   ReactDOM.render(
     <React.StrictMode>
       <ConvexProvider client={convex}>
         <App />
       </ConvexProvider>
     </React.StrictMode>,
     document.getElementById('root')
   );
   ```

2. **Create Convex Handlers:**

   Inside the `src/convex` directory, create a file named `notes.ts`:
   ```ts
   import { mutation, query } from "./_generated/server";
   import { v } from "convex/values";

   export const getNotes = query({
     args: {},
     handler: async (ctx) => {
       return await ctx.db.query("notes").collect();
     },
   });

   export const addNote = mutation({
     args: { content: v.string(), title: v.optional(v.string()) },
     returns: v.null(),
     handler: async (ctx, { content, title }) => {
       const note = { content, title: title || 'Untitled' };
       await ctx.db.insert("notes", note);
     },
   });
   ```

3. **Use Convex Handlers in React Components:**

   Create or modify `App.js` or `App.tsx`:
   ```jsx
   import React, { useState } from 'react';
   import { useQuery, useMutation } from "convex/react";
   import { api } from "./convex/_generated/api";

   function App() {
     const notes = useQuery(api.notes.getNotes);
     const addNote = useMutation(api.notes.addNote);

     const [content, setContent] = useState('');
     const [title, setTitle] = useState('');

     const handleSubmit = async (e) => {
       e.preventDefault();
       if (content) {
         await addNote({ content, title });
         setContent('');
         setTitle('');
       }
     };

     return (
       <div className="App">
         <h1>Notes</h1>
         <form onSubmit={handleSubmit}>
           <input
             type="text"
             value={title}
             onChange={e => setTitle(e.target.value)}
             placeholder="Title"
           />
           <textarea
             value={content}
             onChange={e => setContent(e.target.value)}
             placeholder="Your note content..."
           ></textarea>
           <button type="submit">Add Note</button>
         </form>
         <ul>
           {notes?.map((note, index) => (
             <li key={index}>
               <h3>{note.title}</h3>
               <p>{note.content}</p>
             </li>
           ))}
         </ul>
       </div>
     );
   }

   export default App;
   ```

With these steps, we've set up a simple React application using Convex to manage and display notes. You can now extend or modify it further based on your needs!