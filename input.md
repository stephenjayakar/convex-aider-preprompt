Hey, so we want to make a project using `convex`, which is a full-stack platform that both has a DB as well as a backend, and is meant for frontend developers.

Specifically, I want you to generate a React App that works with `convex` in a first-class way. We'll start with some examples + how to set up `convex` in an app

# How to set up convex in a react app

You already probably know how to set up a basic `react` app that doesn't have `convex`. Assuming we have one, adding `convex` to an app is as simple as this:

```sh
npm install convex
npx convex dev
```

This will prompt the user to set up the `convex` app w/ the backend & authenticate. It will also create the `src/convex` directory.

# How to plug in Convex into the App

You have to wrap your app with the `ConvexProvider`. Something like this:

```jsx
import { ConvexProvider, ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(process.env.REACT_APP_CONVEX_URL);
root.render(
  <React.StrictMode>
    <ConvexProvider client={convex}>
      <App />
    </ConvexProvider>
  </React.StrictMode>
);
```

# How to query / mutate with Convex

Remember, Convex is a backend + DB. So we want to be able to store & fetch data. The following example is inside `src/convex`, which holds server-side `convex` handler code for reading & writing documents.

```jsx
// convex/tasks.ts
import { query, mutation } from "./_generated/server";

export const get = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect();
  },
});

export const send = mutation({
  args: { body: v.string(), author: v.string() },
  returns: v.null(),
  handler: async (ctx, { body, author }) => {
    const message = { body, author };
    await ctx.db.insert("tasks", message);
  },
});
```

# How to wire that data into a React component

```jsx
// YourComponent.tsx (or .jsx)
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

function YourComponent() {
  const tasks = useQuery(api.tasks.get);
  const addTask = useMutation(api.tasks.send);

  // Use tasks and addTask in your component...
}
```

So now you can use `tasks` within a JSX component like normal. Calling `addTask` will rerender everything.

