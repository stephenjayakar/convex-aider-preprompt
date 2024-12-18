It made one mistake. It created `Notes.jsx` in `src/components`. When it tried to import convex, it didn't go the right amount up:

`import { api } from '../../convex/_generated/api';` is the correct line, it was missing one `..`


