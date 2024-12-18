To create a Convex app that lets you add and store notes, here's a step-by-step guide. This will include the necessary files and their content, along with the terminal commands you'll need to use. We'll start by setting up the React app using Vite, installing Convex, and then creating the necessary components and hooks to handle notes.

### Step 1: Set Up the React App

1. **Create the React project using Vite**:

   ```bash
   npm create vite@latest my-notes-app --template react
   cd my-notes-app
   ```

2. **Install Convex**:

   ```bash
   npm install convex
   npx convex dev
   ```

   The second command will guide you through setting up a Convex app. It will also create a `src/convex` directory.

### Step 2: Set Up Convex in Your React App

1. **Modify `main.jsx` to include `ConvexProvider`**:

   Create or update `src/main.jsx` to wrap your application with `ConvexProvider`.

   ```jsx
   import React from 'react';
   import ReactDOM from 'react-dom';
   import { ConvexProvider, ConvexReactClient } from 'convex/react';
   import App from './App';

   const convex = new ConvexReactClient(process.env.REACT_APP_CONVEX_URL);

   ReactDOM.createRoot(document.getElementById('root')).render(
     <React.StrictMode>
       <ConvexProvider client={convex}>
         <App />
       </ConvexProvider>
     </React.StrictMode>
   );
   ```

### Step 3: Create Convex Backend Logic

1. **Create Convex functions for notes**:

   Create a file `src/convex/notes.ts` for server-side query and mutation handlers.

   ```ts
   // src/convex/notes.ts
   import { mutation, query } from "./_generated/server";
   import { v } from 'convex/values';

   export const getNotes = query({
     args: {},
     handler: async (ctx) => {
       return await ctx.db.query("notes").collect();
     },
   });

   export const addNote = mutation({
     args: { content: v.string() },
     handler: async (ctx, { content }) => {
       const note = { content, createdAt: new Date() };
       await ctx.db.insert("notes", note);
     },
   });
   ```

### Step 4: Create the React Component

1. **Create `Notes.js` component**:

   Create a file `src/Notes.jsx` for the Notes component.

   ```jsx
   // src/Notes.jsx
   import React, { useState } from 'react';
   import { useQuery, useMutation } from 'convex/react';
   import { api } from './convex/_generated/api';

   function Notes() {
     const [noteContent, setNoteContent] = useState('');
     const notes = useQuery(api.notes.getNotes);
     const addNote = useMutation(api.notes.addNote);

     const handleAddNote = async () => {
       if (noteContent.trim() !== '') {
         await addNote({ content: noteContent });
         setNoteContent('');
       }
     };

     return (
       <div>
         <h1>Notes</h1>
         <ul>
           {notes && notes.map((note, index) => (
             <li key={index}>{note.content}</li>
           ))}
         </ul>
         <input
           type="text"
           value={noteContent}
           onChange={(e) => setNoteContent(e.target.value)}
           placeholder="Write a note..."
         />
         <button onClick={handleAddNote}>Add Note</button>
       </div>
     );
   }

   export default Notes;
   ```

### Step 5: Update App Component

1. **Update your `App.jsx` to use the `Notes` component**:

   ```jsx
   // src/App.jsx
   import React from 'react';
   import Notes from './Notes';

   function App() {
     return (
       <div className="App">
         <Notes />
       </div>
     );
   }

   export default App;
   ```

### Final Step: Running the Application

1. **Start your development server**:

   ```bash
   npm run dev
   ```

After following these steps, you should have a fully functional React app with Convex that allows you to add and store notes. The app will fetch notes from the backend and display them. You can add new notes through an input field, which will update the list of notes in real-time.
