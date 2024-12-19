Now this is interesting. We got a type error

```
Uncaught (in promise) Error: [CONVEX M(notes:addNote)] [Request ID: ed6f306b151b1514] Server Error
Uncaught Error: Date "2024-12-18T23:57:02.991Z" is not a supported Convex type (present at path .timestamp in original object {"title":"hello world","content":"this is content\n","timestamp":"2024-12-18T23:57:02.991Z"}). To learn about Convex's supported types, see https://docs.convex.dev/using/types.
    at convexToJsonInternal (../node_modules/convex/src/values/value.ts:339:6)
    at convexToJsonInternal (../node_modules/convex/src/values/value.ts:350:15)
    at convexToJson (../node_modules/convex/src/values/value.ts:417:0)
    at insert (../node_modules/convex/src/server/impl/database_impl.ts:95:3)
    at insert [as insert] (../node_modules/convex/src/server/impl/database_impl.ts:131:12)
    at handler (../convex/notes.ts:12:11)
```

