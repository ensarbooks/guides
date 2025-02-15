# Building a Workflow UI Application with React, TypeScript, React Flow, and Drag-and-Drop

## Introduction

A **Workflow UI** application allows users to visually create and manage workflows or processes by connecting **nodes** (representing tasks or steps) with **edges** (connections). This is often seen in tools like automation builders or flowchart editors. We will use **ReactJS** – a popular library for building dynamic UIs – as our foundation, leveraging **TypeScript** for type safety and maintainability. TypeScript is a statically typed superset of JavaScript that adds compile-time type checking and other advanced features to catch errors early ([TypeScript vs JavaScript - A Detailed Comparison | Refine](https://refine.dev/blog/javascript-vs-typescript/#:~:text=TypeScript%20is%20a%20statically%20typed,which%20JavaScript%20developers%20would%20find)). In large-scale apps, TypeScript improves developer productivity and code quality by making data structures and functions explicit ([TypeScript - Material UI](https://mui.com/material-ui/guides/typescript/?srsltid=AfmBOopqIT3F3NtLb8s6ZuvPcN_q1Zk_nxuorFwQP_VyEDcBVOa7cLDJ#:~:text=You%20can%20add%20static%20typing,code%20quality%20thanks%20to%20TypeScript)).

Key libraries in our stack include **React Flow**, **Material-UI (MUI)**, and a drag-and-drop library. **React Flow** is a specialized library for building node-based editors and interactive diagrams ([Node-Based UIs in React - React Flow](https://reactflow.dev/#:~:text=Wire%20Your%20Ideas%20with%20React,Flow)). It provides a highly customizable React component to render nodes and edges, and comes with many features out-of-the-box. For example, React Flow supports dragging nodes, zooming/panning the viewport, multi-selecting elements, and adding/removing connections without extra code ([Node-Based UIs in React - React Flow](https://reactflow.dev/#:~:text=Ready%20out)). It also allows custom node and edge types, meaning we can define how each node looks and behaves using our own React components ([Introduction - React Flow](https://reactflow.dev/learn/concepts/introduction#:~:text=React%20Flow%20is%20a%20library,controls%20out%20of%20the%20box)). React Flow is designed for performance – it only re-renders nodes that change and only displays nodes in the current viewport for efficiency ([Introduction - React Flow](https://reactflow.dev/learn/concepts/introduction#:~:text=Customizable%3A%20React%20Flow%20supports%20custom,bespoke%20logic%20to%20node%20edges)). This makes it suitable for complex workflows with many elements.

We'll use **Material-UI (MUI)** to build the core user interface. Material-UI is an open-source React component library implementing Google’s Material Design system ([Material UI: React components that implement Material Design](https://mui.com/material-ui/?srsltid=AfmBOopHf2hL9Ll6_Ul8Ds7scigiV894itvcwNA3GZPxtWIa23I1DqG7#:~:text=Material%20UI%20is%20an%20open,production%20out%20of%20the%20box)). It provides a robust collection of pre-designed, themable components – from basic buttons and form inputs to complex components like tables and dialogs – that we can leverage to create a clean, responsive application UI ([Mastering Modern UI Development: A Comprehensive Guide to Using Material-UI with React - DEV Community](https://dev.to/christopherthai/mastering-modern-ui-development-a-comprehensive-guide-to-using-material-ui-with-react-9d6#:~:text=One%20of%20the%20standout%20features,to%20your%20brand%E2%80%99s%20unique%20aesthetic)). By using MUI, we adhere to proven design principles and get a consistent look-and-feel without building every component from scratch. MUI components are highly customizable and work well on different screen sizes out-of-the-box, which will help ensure our workflow editor is user-friendly and accessible ([Mastering Modern UI Development: A Comprehensive Guide to Using Material-UI with React - DEV Community](https://dev.to/christopherthai/mastering-modern-ui-development-a-comprehensive-guide-to-using-material-ui-with-react-9d6#:~:text=Material,various%20screen%20sizes%20and%20resolutions)).

For drag-and-drop interactions, we want to enable users to drag elements (like new nodes) from a sidebar into the React Flow canvas, and perhaps drag nodes within the canvas as well. React Flow natively supports dragging nodes **within** the canvas, but dragging items **from outside** (e.g., from a sidebar into the canvas) is **not built-in** ([Drag and Drop - React Flow](https://reactflow.dev/examples/interaction/drag-and-drop#:~:text=A%20drag%20and%20drop%20user,draggable)). We will implement this ourselves using a drag-and-drop library. Two popular choices are **DnD Kit** and **React Beautiful DnD**:

- **DnD Kit**: a modern, lightweight drag-and-drop toolkit for React. It is modular, accessible, and extensible ([dnd kit – a modern drag and drop toolkit for React](https://dndkit.com/#:~:text=A%20lightweight%2C%20performant%2C%20accessible%20and,drop%20toolkit%20for%20React)). DnD Kit exposes hooks (like `useDraggable` and `useDroppable`) to turn any component into a drag source or drop target, giving fine-grained control over behavior ([Overview | @dnd-kit – Documentation](https://docs.dndkit.com/#:~:text=,create%20additional%20wrapper%20DOM%20nodes)) ([Overview | @dnd-kit – Documentation](https://docs.dndkit.com/#:~:text=,lists%2C%202D%20Games%2C%20and%20more)). It supports multiple input methods (mouse, touch, keyboard) and custom collision detection algorithms, making it very flexible for complex interfaces ([Overview | @dnd-kit – Documentation](https://docs.dndkit.com/#:~:text=,lists%2C%202D%20Games%2C%20and%20more)).
- **React Beautiful DnD**: a higher-level library originally from Atlassian, focused on easy drag-and-drop for lists and content reordering. It provides an intuitive API to build drag-and-drop functionality with excellent default behavior and aesthetics ([Using React Beautiful DnD to Implement Drag and Drop](https://pieces.app/blog/implement-react-beautiful-dnd#:~:text=React%20Beautiful%20DnD%20is%20a,flexibility%20and%20offers%20many%20features)). React Beautiful DnD is known for its smooth user experience and flexibility to customize as needed ([Using React Beautiful DnD to Implement Drag and Drop](https://pieces.app/blog/implement-react-beautiful-dnd#:~:text=React%20Beautiful%20DnD%20is%20a,flexibility%20and%20offers%20many%20features)). (Note: React Beautiful DnD has been deprecated in favor of newer solutions, but it’s still used in many projects.)

In this guide, we'll use **DnD Kit** for implementing drag-and-drop, given its performance and flexibility, but the concepts would be similar with any library. We’ll also integrate everything with Material-UI – for instance, our drag handles and drop areas will be MUI components (like lists, cards, etc.), ensuring the UI remains consistent.

Finally, we will cover how to manage the application **state** (using Context API or a state library like Zustand/Redux), how to **optimize performance** as the app grows, how to **test and debug** the application, and best practices for **deployment** to production. By the end of this step-by-step guide, you (as an advanced developer) should have a clear blueprint for building a scalable Workflow Editor UI with React and these powerful libraries.

## Project Setup

Let's start by setting up the development environment and scaffolding the project. We assume you have a recent version of **Node.js** and **npm** (or yarn/pnpm) installed on your machine ([Node-Based UIs in React - React Flow](https://reactflow.dev/#:~:text=Getting%20Started%20with%20React%20Flow)).

**1. Initialize a React + TypeScript project:** We need a React app with TypeScript support. You can use a tool like **Create React App** or **Vite**. For example, to use Vite (which is fast and minimal):

```bash
# Using npm:
npm create vite@latest my-workflow-app -- --template react-ts

# Or using yarn:
yarn create vite my-workflow-app --template react-ts
```

This will create a new directory `my-workflow-app` with a basic React + TypeScript setup. If you prefer Create React App, you can run:

```bash
npx create-react-app my-workflow-app --template typescript
```

Either approach gives us a starter project with TypeScript configured. Once created, navigate into the project folder and install dependencies.

**2. Install React Flow:** React Flow is not part of the default template, so add it via npm or yarn. React Flow is published on npm (the current stable version is v11) ([reactflow - npm](https://www.npmjs.com/package/reactflow#:~:text=11)). Install it along with its peer dependencies:

```bash
npm install reactflow
# or: yarn add reactflow
```

_(Note: For React Flow v12 and above, the package name has changed to `@xyflow/react`. If using v12, you would do `npm install @xyflow/react` as per the docs ([Quickstart - React Flow](https://reactflow.dev/learn#:~:text=React%20Flow%20is%20published%20on,ahead%20and%20add%20it%20next)). In this guide, we'll assume v11 for simplicity and use `reactflow`.)_

After installing, confirm that React Flow was added by checking `package.json` dependencies or running `npm ls reactflow`.

**3. Install Material-UI:** Material-UI (MUI) has several packages. The core components are in `@mui/material`, and it requires emotion (for styling) as peer dependencies. Install them:

```bash
npm install @mui/material @emotion/react @emotion/styled
```

This brings in MUI Core ([Material UI: React components that implement Material Design](https://mui.com/material-ui/?srsltid=AfmBOopHf2hL9Ll6_Ul8Ds7scigiV894itvcwNA3GZPxtWIa23I1DqG7#:~:text=Material%20UI%20is%20an%20open,production%20out%20of%20the%20box)) ([Material UI: React components that implement Material Design](https://mui.com/material-ui/?srsltid=AfmBOopHf2hL9Ll6_Ul8Ds7scigiV894itvcwNA3GZPxtWIa23I1DqG7#:~:text=%24%20npm%20install%20%40mui%2Fmaterial%20%40emotion%2Freact,emotion%2Fstyled)). Optionally, you can also install MUI icons (`@mui/icons-material`) if you plan to use icons for node types or toolbar buttons.

**4. Install Drag-and-Drop library:** We will use DnD Kit for drag-and-drop. Install the core package and the additional presets if needed:

```bash
npm install @dnd-kit/core @dnd-kit/sortable
```

`@dnd-kit/core` provides the primitives (DndContext, useDraggable, useDroppable, etc.), and `@dnd-kit/sortable` is an add-on for sortable lists (which might not be needed for our use-case, but could be useful if we want reordering functionality). Alternatively, if you chose to use react-beautiful-dnd instead, you'd do `npm install react-beautiful-dnd` ([Using React Beautiful DnD to Implement Drag and Drop](https://pieces.app/blog/implement-react-beautiful-dnd#:~:text=npm%20install%20react)), but we'll proceed with DnD Kit.

**5. Optional – State management library:** If you anticipate using a global state store (Redux or Zustand), you can install it now. For example, to use Zustand (a lightweight state library that works well with React Flow ([Using a State Management Library - React Flow](https://reactflow.dev/learn/advanced-use/state-management#:~:text=In%20this%20guide%2C%20we%20explain,as%20Redux%2C%20Recoil%20or%20Jotai))):

```bash
npm install zustand
```

You can also install Redux (`npm install redux react-redux`) if you plan to use it. This guide will later illustrate state management with context or Zustand, so Redux is optional.

**6. Configure TypeScript settings:** The template comes with a `tsconfig.json`. Ensure it has strict type-checking enabled. For example, options like `"strict": true`, `"noImplicitAny": true`, `"strictNullChecks": true` should be set ([TypeScript - Material UI](https://mui.com/material-ui/guides/typescript/?srsltid=AfmBOopqIT3F3NtLb8s6ZuvPcN_q1Zk_nxuorFwQP_VyEDcBVOa7cLDJ#:~:text=For%20types%20to%20work%2C%20it%27s,tsconfig.json)). MUI requires TS >= 4.7, so make sure your TypeScript version meets that ([TypeScript - Material UI](https://mui.com/material-ui/guides/typescript/?srsltid=AfmBOopqIT3F3NtLb8s6ZuvPcN_q1Zk_nxuorFwQP_VyEDcBVOa7cLDJ#:~:text=Material%C2%A0UI%20requires%20a%20minimum%20version,React%20App%20with%20TypeScript%20example)) (the installed version in the template usually is fine). If not, update TypeScript (`npm install --save-dev typescript@latest`).

**7. Project structure setup:** Open the project in your code editor. You'll see a `src` directory with files like `main.tsx`/`index.tsx`, `App.tsx`, etc. For now, let's remove boilerplate code that we don't need (like the default CSS or logo). We want a clean starting point. In `App.tsx`, you can replace the content with a simple placeholder (e.g., a div or Typography that says "Workflow Editor App"). We will build out the App component step by step.

**8. Verify the setup:** Run the development server:

```bash
npm run dev   # for Vite
# or for CRA:
npm start
```

Open the app in your browser (usually at http://localhost:3000 for CRA or 5173 for Vite). You should see the placeholder text you put in App. There should be no errors in the console. This confirms React, TypeScript, and our dependencies are all configured correctly.

Now we have an empty React/TypeScript application with React Flow, Material-UI, and DnD kit installed. Next, we'll plan the application architecture to ensure the project remains scalable as we add features.

## Application Architecture

Before diving into coding features, it's important to design a clear architecture for the application. A workflow editor can become complex, so structuring the code will help in maintenance and scalability. Here are some **principles and patterns** we'll use:

- **Feature-Based Organization:** Organize the code by feature/domain rather than by type. For easy scalability and maintenance, keep most code in a `src/features` folder, where each feature (or module) contains its own components, state, hooks, and utilities ([bulletproof-react/docs/project-structure.md at master · alan2207/bulletproof-react · GitHub](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md#:~:text=For%20easy%20scalability%20and%20maintenance%2C,scalability%20in%20the%20application%27s%20architecture)) ([bulletproof-react/docs/project-structure.md at master · alan2207/bulletproof-react · GitHub](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md#:~:text=src%2Ffeatures%2Fawesome,for%20a%20specific%20feature)). For example, we might have a `features/workflow` module for the main workflow editor components, a `features/nodes` module for node-specific components or logic, etc. This separation means all files related to a feature live together, making it easier to navigate and modify the feature without affecting unrelated parts.

- **Shared vs. Feature Components:** Components that are generic or used across the app (buttons, layout containers, etc.) can reside in a global `components/` directory, whereas feature-specific components stay within the feature folder ([bulletproof-react/docs/project-structure.md at master · alan2207/bulletproof-react · GitHub](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md#:~:text=%2B,libraries%20preconfigured%20for%20the%20application)) ([bulletproof-react/docs/project-structure.md at master · alan2207/bulletproof-react · GitHub](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md#:~:text=For%20easy%20scalability%20and%20maintenance%2C,scalability%20in%20the%20application%27s%20architecture)). For instance, a custom node component that is only used in the workflow editor can be in `features/workflow/NodeItem.tsx`, but a generic modal dialog component could be in `components/ConfirmationDialog.tsx`. This prevents mixing feature-specific code with common code and keeps the project organized.

- **Container/Presentational Pattern:** Separate **container** (smart) components from **presentational** (dumb) components where applicable ([Building Scalable React Applications: Design Patterns and Architecture - DEV Community](https://dev.to/drruvari/building-scalable-react-applications-design-patterns-and-architecture-39a0#:~:text=,UI%20based%20on%20props%20received)). Container components handle state, data fetching, and logic, and pass data down to presentational components, which are primarily for rendering UI. In our case, a container component might be one that orchestrates the workflow canvas state (nodes and edges) and provides handlers for events, while a presentational component could be a sidebar panel or a form that simply displays data from props. This pattern helps manage complexity by isolating concerns. For example, if we had a list of workflow templates loaded from an API, a container would fetch that list and pass it to a presentational `<TemplateList>` component for display.

- **Context for Shared State:** Identify what state needs to be global. For instance, if multiple parts of the app need access to the workflow data (nodes/edges) or the currently selected node, it might be wise to use React Context or a global store. We can create a `WorkflowContext` to provide the nodes, edges, and update functions to any component that needs it, instead of prop-drilling those through many layers. In a larger app, context or a state library will simplify state updates from different components (we'll detail state management later).

- **Directory Structure:** A possible structure under `src/` could be:

  ```
  src/
    components/      # Reusable components (not tied to one feature)
    features/
      workflow/      # Feature: Workflow editor
        components/  # sub-components of workflow feature
        hooks/       # any custom hooks for this feature
        context.ts   # context provider for workflow state (if using context)
        WorkflowPage.tsx  # main page component for the workflow editor
      nodes/         # Feature: Node definitions (if separated)
        ...
    stores/          # Global state stores (if using Zustand or Redux slices)
    utils/           # Utility functions
    App.tsx
    main.tsx (or index.tsx)
  ```

  This is just one way; the key is to keep related code together and separation of concerns clear. As an example, the **bulletproof-react** repo suggests a similar structure with an `app/` for app-level setup (like providers, routes), `features/` for feature modules, and so on ([bulletproof-react/docs/project-structure.md at master · alan2207/bulletproof-react · GitHub](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md#:~:text=src%20%7C%20%2B,based%20on%20meta%20framework%20used)) ([bulletproof-react/docs/project-structure.md at master · alan2207/bulletproof-react · GitHub](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md#:~:text=%2B,global%20state%20stores)).

- **Scalability considerations:** Think ahead about adding features like saving/loading workflows, multi-user collaboration, etc. Even if we don’t implement them now, a clean architecture will make it easier to add them later. For instance, if we plan to have different pages (home, workflow editor, settings), using a router (React Router) and organizing pages into a `routes` or `pages` directory might be beneficial ([bulletproof-react/docs/project-structure.md at master · alan2207/bulletproof-react · GitHub](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md#:~:text=%2B,application%20router%20configuration)). In a single-page app like ours (just the editor), we may not need routing initially, but it's easy to add if structured well.

- **Separation of Styling:** We will use MUI’s styling solution primarily, but ensure style definitions (custom `sx` props or styled components) are kept close to the component they style. If there are global style overrides, keep them in a dedicated theme or CSS file.

In summary, plan your **data flow** and **dependencies**: The React Flow component will need data (nodes/edges) and provide events (like onConnect). The sidebar will need to know what node types it can create. A context or store can mediate between these. The architecture might look like:

- **App.tsx:** Sets up high-level providers (ThemeProvider for MUI, possibly ReactFlowProvider, WorkflowContext Provider if using context, etc.) and renders the main `WorkflowEditor` component.
- **WorkflowEditor (WorkflowPage.tsx)**: A container that renders the layout (sidebar + canvas + any other panels). It uses context/store to fetch the nodes/edges state and passes them to the ReactFlow canvas component. It also provides handlers for adding nodes (when something is dropped) or modifying edges.
- **Sidebar.tsx:** A component in the workflow feature that lists available node types. It interacts with drag-and-drop (by making items draggable and possibly calling context actions to add a node).
- **CanvasArea/WorkflowCanvas.tsx:** The component wrapping `ReactFlow`. It receives nodes and edges (from context or props), and defines event handlers (onNodesChange, onConnect, onDrop, etc.), which in turn update the state via context or dispatch actions to the store.
- **NodeComponents:** If we have custom node types, each can be a presentational component (e.g., `TaskNode.tsx` that defines how a "Task" node looks). These might use MUI Paper/Card components internally for styling. We’ll register them with React Flow’s `nodeTypes` so React Flow knows to use them.

This architecture ensures that each part of the UI is encapsulated: the sidebar doesn’t directly manipulate the canvas, it just initiates drags; the canvas doesn’t directly know about the sidebar, it just handles drops; the shared state (nodes/edges) is the source of truth that both use via context or store.

As we proceed, we will create these components and context accordingly. The next step is to start building the core UI layout using Material-UI, which will give us the scaffolding (AppBar, Sidebar, Canvas area) to put our workflow editor components in place.

## Building the Core UI

With the project structure in mind, let's build the fundamental UI layout using Material-UI. The goal here is to create the primary layout: a top navigation bar, a sidebar for dragging nodes, and a main canvas area where the workflow graph will be displayed. We will use Material-UI components to achieve a professional look easily.

**1. Set up the Theme (optional):** Material-UI comes with a default theme, but we can customize it if needed. For now, we can wrap our app in MUI’s `ThemeProvider` and `CssBaseline` for consistent styling. In `main.tsx` (or `index.tsx` for CRA), add:

```tsx
import { ThemeProvider, createTheme, CssBaseline } from "@mui/material";
// ... other imports

const theme = createTheme({
  palette: {
    mode: "light", // or 'dark' – could allow theme switching
    primary: { main: "#1976d2" },
    // customize as needed
  },
});

root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>
);
```

This ensures Material-UI styles are applied across the app and we have a baseline of global styles reset. (We import `CssBaseline` to normalize browser styles according to Material Design.)

**2. Layout structure with AppBar and Drawer:** In `App.tsx` (or better, in a new component like `WorkflowPage.tsx` under `features/workflow/`), create the layout:

- A **top AppBar**: This will contain the application title or navigation actions.
- A **left Drawer (sidebar)**: This will contain a list of node types that can be dragged into the workflow.
- A **main content area**: This is where the React Flow graph will be rendered.

Let's create a component `WorkflowPage.tsx`:

```tsx
import {
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  Box,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";

const drawerWidth = 240; // width in pixels for sidebar

export default function WorkflowPage() {
  return (
    <Box sx={{ display: "flex", height: "100vh" }}>
      {/* Top AppBar */}
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Workflow Editor
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Sidebar Drawer */}
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar /> {/* to push content below AppBar */}
        <Box sx={{ overflow: "auto" }}>
          <List>
            {/* Example node type items */}
            {["Start", "Task", "Decision", "End"].map((text) => (
              <ListItem
                key={text}
                draggable
                onDragStart={(e) => handleDragStart(e, text)}
                button
              >
                <ListItemText primary={text} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      {/* Main content area for React Flow */}
      <Box component="main" sx={{ flexGrow: 1, p: 2, ml: `${drawerWidth}px` }}>
        <Toolbar /> {/* spacer to account for fixed AppBar */}
        {/* React Flow canvas will go here */}
        <div
          id="canvas-wrapper"
          style={{ width: "100%", height: "80vh", border: "1px solid #ccc" }}
        >
          Canvas goes here
        </div>
      </Box>
    </Box>
  );
}
```

In this snippet:

- We used an MUI `<AppBar>` with a `<Toolbar>` and some text. The `position="fixed"` keeps it on top. We increased its z-index to sit above the drawer.
- The `<Drawer variant="permanent">` creates a sidebar that is always visible (like a persistent sidebar). We set its width and made sure the paper element (the drawer itself) has that width. We add a `<Toolbar />` inside it as well to push its content below the AppBar (since the AppBar is fixed at the top, its height would overlap content).
- Inside the drawer, we used a `<List>` with `<ListItem>`s to represent node types. Each ListItem is marked `draggable` and has an `onDragStart` handler (we will implement `handleDragStart` soon) so that users can drag them. The `button` prop on ListItem just gives it a hover effect (since they function like menu items).
- The main content `<Box component="main">` is the central area. We gave it `flexGrow: 1` so it expands to fill space, some padding, and a left margin equal to drawerWidth to ensure content isn’t under the drawer (this margin plus the Drawer’s fixed width align the content). We inserted another `<Toolbar />` at the top of main content to give top padding equal to the AppBar's height (aligning content below the AppBar).
- Finally, we have a placeholder `<div id="canvas-wrapper">` that currently just has a border and height. This is where our React Flow component will be rendered. For now, it's a static placeholder ("Canvas goes here").

Now, let's implement `handleDragStart`. This function will initiate a drag of a node type from the sidebar. We can define it within `WorkflowPage`:

```tsx
const handleDragStart = (
  event: React.DragEvent<HTMLDivElement>,
  nodeType: string
) => {
  event.dataTransfer.setData("application/reactflow", nodeType);
  event.dataTransfer.effectAllowed = "move";
};
```

This uses the native HTML5 Drag and Drop API: we attach data to the drag event with a custom MIME type `'application/reactflow'` (this is a convention used by React Flow examples ([React Flow - Drag and Drop Example](https://v9.reactflow.dev/examples/drag-and-drop/#:~:text=const%20onDragStart%20%3D%20,))) carrying the type of node. We also set `effectAllowed` to 'move' to indicate the intended drag operation.

Now our sidebar items can be dragged and they carry their type information. (We used simple text like "Start", "Task" as identifiers; in a real app, you might use more specific keys or an enum of node types.)

The core UI now has:

- A top bar with title.
- A sidebar with draggable items.
- A main area for the canvas.

**3. Make the canvas fill the viewport:** We gave the canvas wrapper a fixed height of 80vh in the snippet just as a placeholder. We likely want the canvas to dynamically fill the remaining space. Because our Box with `display: 'flex'` and `height: '100vh'` includes everything, the main content Box has height 100vh as well but minus padding/margin for top bar. One way is to set the canvas div to `height: calc(100vh - 64px)` (if the AppBar is 64px high by default for desktop) to fill the rest. Alternatively, once we integrate React Flow, we will set its container to 100% width and height. We can adjust styling then.

**4. Responsive considerations:** The drawer is `permanent` which is fine for a desktop view. If you want this to be responsive (collapsible on small screens), MUI has `temporary` or `responsive` drawer variants. For simplicity, we keep it always open. (Advanced: you could integrate a toggle button in the AppBar to open/close the drawer on mobile, but we'll not focus on that here.)

**5. Use MUI components for Node representation:** At this stage, our ListItems in the sidebar are plain text. We could enhance them, e.g., use MUI Icons alongside text to make it more visual. For example, a "Start" node could have a Play icon, a "Decision" node could have a fork icon. If using `@mui/icons-material`, we could import icons and render inside the ListItem. But this is cosmetic – the main point is that these items are draggable sources.

We should now render `WorkflowPage` in our App. In `App.tsx`, simply return `<WorkflowPage />`. Also ensure to import ReactFlow styles globally (we'll do that in the integration section). For now, if you run the app, you should see the UI layout: a sidebar with items, and a blank canvas area. You can try dragging an item – nothing will happen on drop yet, but you should see the drag preview of the item text.

At this point, we have a well-structured UI. The Material-UI components give us a professional look, and our layout is in place. Next, we’ll integrate **React Flow** into the canvas area so that we have an actual interactive workflow graph.

## React Flow Integration

Now it's time to embed the React Flow component into our application to handle the workflow diagram. React Flow will manage the rendering of nodes and edges and provide interactivity (moving nodes, connecting them, etc.). We'll set up React Flow, define some initial nodes/edges, and connect it with our drag-and-drop logic.

**1. Import and setup React Flow component:** In the component where we want the canvas (our `WorkflowPage` main area), import React Flow and its related hooks:

```tsx
import ReactFlow, {
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
} from "reactflow";
import "reactflow/dist/style.css";
```

We import:

- `ReactFlow` – the main component.
- `Background` and `Controls` – built-in plugins for a grid background and zoom controls.
- Hooks `useNodesState` and `useEdgesState` – convenience hooks to manage state of nodes and edges.
- `addEdge` – a helper to easily add a new edge to the state.
- We also import the CSS for React Flow (important for it to display correctly) ([Quickstart - React Flow](https://reactflow.dev/learn#:~:text=There%20are%20a%20few%20things,to%20pay%20attention%20to%20here)).

**2. Define initial state for nodes and edges:** For example, we might start with no edges and maybe one starter node (or even no nodes). Let's do a simple initial node to see something:

```tsx
const initialNodes: Node[] = [
  {
    id: "node-1",
    type: "input", // built-in type for an input node (maybe styled differently by ReactFlow)
    data: { label: "Start Node" },
    position: { x: 250, y: 100 },
  },
];
const initialEdges: Edge[] = [];
```

_(Ensure to import or define the `Node` and `Edge` types from React Flow for TypeScript – they can be imported from 'reactflow' as well.)_

Inside our component, use the hooks:

```tsx
const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
```

These hooks manage the state and also give us change handler functions (`onNodesChange`, `onEdgesChange`) that we will pass to ReactFlow component. React Flow calls those when nodes or edges are moved/edited, allowing us to update our state.

**3. Implement connection handling:** Users will connect nodes by dragging a connector between them in the UI. React Flow provides an `onConnect` event that gives us the connection (source and target node ids). We can handle it by adding a new edge. We'll define:

```tsx
const onConnect = useCallback(
  (connection: Connection) => setEdges((eds) => addEdge(connection, eds)),
  [setEdges]
);
```

Here, `addEdge` will create an Edge object from the given connection (which includes source, target, etc.) and add it to our existing edges state ([Drag and Drop - React Flow](https://reactflow.dev/examples/interaction/drag-and-drop#:~:text=const%20onConnect%20%3D%20useCallback,)). We wrap in `useCallback` to avoid recreating the function on every render (performance optimization).

**4. Render ReactFlow inside our canvas area:** Replace the placeholder div with the ReactFlow component:

```tsx
<div id="canvas-wrapper" style={{ width: "100%", height: "80vh" }}>
  <ReactFlow
    nodes={nodes}
    edges={edges}
    nodeTypes={nodeTypes} /* optional custom nodes, see below */
    onNodesChange={onNodesChange}
    onEdgesChange={onEdgesChange}
    onConnect={onConnect}
    onDrop={onDrop} /* will implement for DnD */
    onDragOver={onDragOver} /* will implement for DnD */
    fitView
  >
    <Controls />
    <Background color="#aaa" gap={16} />
  </ReactFlow>
</div>
```

We pass in our state (`nodes`, `edges`) and the handlers. We also include `fitView` prop which makes the view adjust to fit all nodes initially. The `<Controls />` adds zoom-in/out and fit buttons, and `<Background />` adds a grid background which is common in workflow editors. The `color` and `gap` props adjust its appearance.

We have placeholders for `nodeTypes`, `onDrop`, `onDragOver` which we'll address:

- `nodeTypes`: React Flow allows custom node rendering. We might not need a custom node yet, but if we want to use MUI components inside nodes, we can define a custom node component and provide it here. For now, we can omit or leave an empty object if not using.
- `onDrop` and `onDragOver`: These are events on the React Flow container to handle dropping external items (for our drag-and-drop from sidebar).

**5. Handle drag-over and drop on the canvas:** To allow dropping, we must prevent the default drag-over behavior (which would deny drops). And on drop, we create a new node at the drop location.

Add to `WorkflowPage` component:

```tsx
const onDragOver = useCallback((event: React.DragEvent) => {
  event.preventDefault();
  event.dataTransfer.dropEffect = "move";
}, []);

const onDrop = useCallback(
  (event: React.DragEvent) => {
    event.preventDefault();
    // Only proceed if dropping a valid draggable from our sidebar
    const nodeType = event.dataTransfer.getData("application/reactflow");
    if (!nodeType) return;

    // get drop position in pixels relative to canvas
    const reactFlowBounds = (
      event.target as HTMLElement
    ).getBoundingClientRect();
    const position = {
      x: event.clientX - reactFlowBounds.left,
      y: event.clientY - reactFlowBounds.top,
    };
    // Create a new node
    const newNode: Node = {
      id: `node_${nodes.length + 1}`,
      type: nodeType === "Start" ? "input" : "default", // for example, map types
      data: { label: `${nodeType} Node` },
      position,
    };
    setNodes((nds) => nds.concat(newNode));
  },
  [nodes, setNodes]
);
```

Explanation:

- `onDragOver`: Called continuously when an item is dragged over the ReactFlow area. We call `event.preventDefault()` to allow dropping, and set the dropEffect to indicate a move.
- `onDrop`: When the user releases the draggable over the ReactFlow area. We first prevent default behavior. Then we check the dataTransfer for our custom type `'application/reactflow'` to ensure this drop originated from our sidebar (and not some other drag). This is how we retrieve the node type that we set in `handleDragStart`. If it's missing, we exit (not a valid drop).
- We calculate the drop position relative to the ReactFlow container. We get the bounding rect of the event target (which should be the container element) and subtract its top-left from the event's clientX/Y to get x,y coordinates **within** the container.
- We then create a `newNode` object with a unique id, set its `type` (for simplicity, we map our sidebar text "Start" to React Flow's built-in 'input' type, others to 'default'. You can define custom logic or a mapping for node types), set the `data.label` to e.g. "Start Node" or "Task Node", and use the position we calculated ([Drag and Drop - React Flow](https://reactflow.dev/examples/interaction/drag-and-drop#:~:text=const%20position%20%3D%20screenToFlowPosition%28,type%7D%20node%60)).
- Finally, we use `setNodes` to add this node to the current list of nodes. We used the functional form `setNodes(nds => nds.concat(newNode))` to append the node.

With this, when a user drops an item from the sidebar onto the canvas, a new node will be created at that drop location.

**6. Wrap with ReactFlowProvider (if needed):** Since we are using ReactFlow within one component and not accessing ReactFlow context outside, we might not need an explicit provider. However, if you run into issues with hooks like useReactFlow (which needs a context), you can wrap your canvas in `<ReactFlowProvider>` as shown in React Flow docs ([Drag and Drop - React Flow](https://reactflow.dev/examples/interaction/drag-and-drop#:~:text=export%20default%20%28%29%20%3D,ReactFlowProvider%3E)):

```tsx
<ReactFlowProvider>
  <ReactFlow ...> ... </ReactFlow>
</ReactFlowProvider>
```

This ensures the internal state context is available. In many simple cases, it's not required to wrap if you only have one ReactFlow instance.

**7. Try it out:** Restart the dev server if needed. In the app, you should now see the initial node ("Start Node") on the canvas (if you added one). You should be able to drag it around, zoom in/out with the controls, etc. These features are built-in to React Flow ([Introduction - React Flow](https://reactflow.dev/learn/concepts/introduction#:~:text=Easy%20to%20use%3A%20React%20Flow,in)). Try dragging a "Task" from the sidebar into the canvas: when you drop it, our `onDrop` should fire and a new node will appear at that location. This demonstrates the integration of our custom drag-and-drop with React Flow’s state.

You can also try connecting nodes: click and drag from the small handle on an 'input' node (if type is 'input' or 'output', React Flow by default gives them connection handles) to another node. The `onConnect` will fire and add an edge, which should render as a line connecting the nodes.

At this stage, we have a functional workflow editor canvas:

- **React Flow** is handling node/edge rendering and movement. It provides smooth dragging and zooming by default.
- **Our code** handles adding new nodes via drag-and-drop from the sidebar.
- We can extend this further by customizing node appearance and adding more interaction (like selecting nodes, deleting nodes, etc.), but let's solidify what we have and manage the state properly.

**8. Customizing Node Components (optional):** By default, React Flow's nodes for type 'default' or 'input' are quite minimal (just display the `data.label`). We might want to use Material-UI to make nodes visually richer. React Flow allows custom node components via the `nodeTypes` prop. For example, we could define:

```tsx
const CustomNode = ({ data }: NodeProps) => {
  return (
    <Paper elevation={3} sx={{ padding: 2 }}>
      <Typography variant="body2">{data.label}</Typography>
    </Paper>
  );
};
const nodeTypes = { default: CustomNode };
```

And pass `nodeTypes={nodeTypes}` to ReactFlow. This would render all 'default' type nodes using our `CustomNode` component (which is using MUI `<Paper>` and `<Typography>`). Ensure to import `Paper` and `Typography`. This way, our nodes could have a card-like appearance. You can create different components for different node `type` if needed (e.g., a different look for 'input' or 'output' nodes).

_(Advanced: We could also add interactivity in nodes – like buttons or menus – for editing node properties. That would require handling events inside the custom node and possibly updating global state. We won't cover full node customization here, but React Flow’s flexibility allows anything from forms inside nodes to resize handles, etc., as needed.)_

We now have the core of our workflow UI functioning. The next big piece is **state management** – currently, our state (nodes and edges) is held in the `WorkflowPage` component via hooks. As the app grows, we may want a more global state solution (especially if other components like a property panel need to access or modify the workflow). We'll explore using context or Zustand for state management next.

## State Management

Managing state in a workflow editor can become complex. We have to keep track of nodes and edges, update them when users interact (move nodes, add connections, delete elements), and possibly track other UI state like selected node, zoom level, etc. Up to now, we used React Flow’s hooks (`useNodesState`, `useEdgesState`) **within a component**, which works for a simple case. But as our application grows, we might want a single source of truth for the workflow state that can be accessed by multiple components (for example, a side panel showing details of the selected node, or a toolbar button that triggers adding a node).

There are a few approaches for state management in React:

- **Lifting state up + passing via props:** We could keep the nodes/edges in a parent (like App or a context provider) and pass them down to WorkflowPage and others. This gets cumbersome as the app grows and more components need the data.
- **React Context**: Provide the state globally. This is a good approach for moderately complex state and avoids prop drilling. We can create a context that holds `{ nodes, edges, setNodes, setEdges, selectedNode, setSelectedNode, ... }` and wrap our component tree with it.
- **State Management Libraries**: Libraries like **Redux** or **Zustand** (or others like Recoil, Jotai) help manage global state with more structure. Redux is powerful for very complex state with predictability (and devtools), but it requires a bit of boilerplate. Zustand is simpler, letting you create a store with a few lines and use it via hooks, which fits nicely with React Flow (which itself uses Zustand internally for its own state) ([Using a State Management Library - React Flow](https://reactflow.dev/learn/advanced-use/state-management#:~:text=In%20this%20guide%2C%20we%20explain,as%20Redux%2C%20Recoil%20or%20Jotai)).

For an advanced application, using a dedicated state library can be beneficial once the state goes beyond just a couple of variables. React Flow’s documentation even provides an example of using Zustand to manage nodes and edges ([Using a State Management Library - React Flow](https://reactflow.dev/learn/advanced-use/state-management#:~:text=As%20demonstrated%20in%20previous%20guides,as%20outlined%20in%20this%20guide)). The idea is to allow parts of the app (like custom node components or sidebars) to update the global state without having to pass callbacks deeply.

Let's outline using **Zustand** for our workflow state:

**1. Create a Zustand store:** We will define a store that holds our nodes, edges, and possibly actions to modify them. Create a file `src/features/workflow/flowStore.ts`:

```ts
import create from "zustand";
import { Node, Edge, Connection } from "reactflow";
import { addEdge } from "reactflow";

interface WorkflowState {
  nodes: Node[];
  edges: Edge[];
  setNodes: (nodes: Node[] | ((nds: Node[]) => Node[])) => void;
  setEdges: (edges: Edge[] | ((eds: Edge[]) => Edge[])) => void;
  onConnect: (connection: Connection) => void;
  // you could also add actions like deleteNode, updateNode, selectNode, etc.
}

export const useWorkflowStore = create<WorkflowState>((set, get) => ({
  nodes: [],
  edges: [],
  setNodes: (nodes) => {
    // nodes can be an array or an updater function
    set((state) => ({
      nodes: typeof nodes === "function" ? nodes(state.nodes) : nodes,
    }));
  },
  setEdges: (edges) => {
    set((state) => ({
      edges: typeof edges === "function" ? edges(state.edges) : edges,
    }));
  },
  onConnect: (connection) => {
    set((state) => ({
      edges: addEdge(connection, state.edges),
    }));
  },
}));
```

In this store:

- `nodes` and `edges` hold the current arrays.
- `setNodes` and `setEdges` allow updating them. They accept either a new array or a function (to mirror how React’s state updater can be functional). We apply the function to the current state to produce the new state.
- `onConnect` uses `addEdge` to add a new edge to the edges list when a connection is made.

We can initialize `nodes` with a default node as before, or start empty and provide a separate function to add a starter node.

We could also add other actions like `addNode(node)` or `removeNode(id)` to encapsulate those operations in the store.

**2. Use the store in components:** In `WorkflowPage`, instead of using `useNodesState`, we can use our store. For example:

```tsx
import { useWorkflowStore } from "./flowStore";

const nodes = useWorkflowStore((state) => state.nodes);
const edges = useWorkflowStore((state) => state.edges);
const setNodes = useWorkflowStore((state) => state.setNodes);
const setEdges = useWorkflowStore((state) => state.setEdges);
const onConnect = useWorkflowStore((state) => state.onConnect);
```

Now, when rendering `<ReactFlow>`, we pass `nodes={nodes}`, `edges={edges}`, `onNodesChange={...}`, etc. But here is a consideration: React Flow’s `useNodesState` was giving us the `onNodesChange` handler which internally calls setNodes. If we are using our own store, we need to implement `onNodesChange` ourselves. React Flow's docs explain that `onNodesChange` is used to handle node drag, node delete, etc., providing changes like position updates or removal info. They supply a utility hook `useNodesState` that returns an `onNodesChange` already wired to update state. We can mimic that with our store:

We can use React Flow's built-in hook even with Zustand, but that would keep state internally. Instead, we can use React Flow’s `useStore` API or manually handle node changes. For simplicity, we might actually still use `useNodesState` and `useEdgesState` for local handling and then sync it to Zustand. However, that could duplicate state.

A straightforward way: we can assign `onNodesChange` to a function that applies the changes to our Zustand state. React Flow provides a utility function type `NodeChange` (with fields describing the change). We can do:

```tsx
const onNodesChange = useCallback(
  (changes: NodeChange[]) => {
    setNodes((nds) => applyNodeChanges(changes, nds));
  },
  [setNodes]
);
```

We would import `applyNodeChanges` from 'reactflow'. This function takes the array of changes and the current nodes, and returns a new nodes array with those changes applied.

Similarly, for `onEdgesChange`:

```tsx
const onEdgesChange = useCallback(
  (changes: EdgeChange[]) => {
    setEdges((eds) => applyEdgeChanges(changes, eds));
  },
  [setEdges]
);
```

Import `applyEdgeChanges` from 'reactflow'.

Now `onNodesChange` and `onEdgesChange` will update our Zustand store state when nodes are moved or removed (for example, deleting a node in React Flow triggers a "remove" change). The Zustand store will update, and since our component is using `useWorkflowStore` to subscribe to `nodes` and `edges`, it will re-render with new state.

Passing `onConnect={onConnect}` directly from the store is fine since we defined `onConnect` to update edges.

With this setup, any part of the app can use `useWorkflowStore` to get or set nodes and edges. For example, if we had a **properties panel** that shows details of the selected node and allows editing its label, that panel could call something like `useWorkflowStore.getState().setNodes(...)` to update the nodes array (maybe find the node by id and change its data). Zustand’s store can be used outside of React components as well (via getState/setState), which is convenient for external logic.

**3. Context API alternative:** If Zustand or Redux is overkill for you, a simpler (but manual) approach is to use React Context. For instance:

```tsx
interface WorkflowContextValue {
  nodes: Node[];
  edges: Edge[];
  setNodes: React.Dispatch<React.SetStateAction<Node[]>>;
  setEdges: React.Dispatch<React.SetStateAction<Edge[]>>;
  // plus any other actions or state like selectedNode, etc.
}
const WorkflowContext = createContext<WorkflowContextValue | undefined>(
  undefined
);

function WorkflowProvider({ children }: { children: React.ReactNode }) {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  // maybe include onConnect similar to above using addEdge and setEdges

  return (
    <WorkflowContext.Provider value={{ nodes, edges, setNodes, setEdges }}>
      {children}
    </WorkflowContext.Provider>
  );
}
```

Then wrap `<WorkflowProvider>` around your app or around the WorkflowPage. Inside any component, use `const ctx = useContext(WorkflowContext)` to get the values. You can then manipulate `ctx.nodes` or call `ctx.setNodes` from different places. This approach works fine for a moderate app, though you'll end up writing some boilerplate for each action (like handling connect, removal, selection, etc., in context).

In general, for advanced applications:

- **Redux** might be chosen if you want predictable state changes, time-travel debugging, or have a large team used to Redux patterns. You would create actions (e.g., ADD_NODE, UPDATE_NODE, REMOVE_NODE, ADD_EDGE, etc.) and a reducer to handle them, and use the React-Redux `Provider` to make the store available. Redux is very robust, but requires writing those action types and reducer logic.
- **Zustand** provides a middle ground: minimal boilerplate, direct mutate via actions, and still gives you the ability to integrate with React DevTools (there’s a middleware for Zustand to connect to Redux DevTools as well).

React Flow’s team chose Zustand for their internal state because of its simplicity and performance, and you can do the same externally ([Using a State Management Library - React Flow](https://reactflow.dev/learn/advanced-use/state-management#:~:text=library%20Zustand,as%20Redux%2C%20Recoil%20or%20Jotai)). As noted in their docs, as your app grows and you need to update state from within individual nodes, passing around functions via props becomes cumbersome – that's when a global state store shines ([Using a State Management Library - React Flow](https://reactflow.dev/learn/advanced-use/state-management#:~:text=As%20demonstrated%20in%20previous%20guides,as%20outlined%20in%20this%20guide)).

For our guide, we won’t fully migrate everything to a Zustand store in code, but it's good to know how to do it. The rest of the guide will assume that either:

- We keep using local state (useNodesState) in the WorkflowPage and maybe use Context to allow other components to access it.
- Or we have integrated Zustand as above, which would behave similarly from the component's perspective.

**4. Selecting and modifying nodes:** A common piece of state is which node is currently selected (clicked on). React Flow can handle selection (if you enable selection on nodes, they can be marked selected and appear with a blue outline). You can get the selected nodes via `onSelectionChange` or using the internal `useStore` hook of React Flow. If using our own state, we might track `selectedNodeId` in our store or context. For example, add `selectedNodeId` and `setSelectedNodeId` in WorkflowState or Context. Then use `onNodeClick` event on ReactFlow (`onNodeClick={(evt, node) => setSelectedNodeId(node.id)}`) to set it. This would allow a separate component, say `<NodeDetailsPanel>`, to consume the selected node ID from context/store and display details (like node type, maybe a form to edit node properties).

**5. Undo/Redo:** With state centralized, implementing undo/redo becomes easier (you can keep a history stack of state or patches). This is advanced functionality; libraries like Redux or Zustand can be extended for this (Redux has middleware for undo/redo, Zustand you can manually handle or use a middleware plugin).

In summary, for state management:

- Start simple (as we did with component state).
- Refactor to context or Zustand when needed to avoid tangled prop chains and to allow multiple components to sync on state.
- Keep in mind React Flow's own state; sometimes you might want to query something from React Flow internal (like whether a node is currently dragging). React Flow offers a hook `useStore` to subscribe to its internal Zustand store for such cases ([useStore - React Flow](https://reactflow.dev/api-reference/hooks/use-store#:~:text=useStore%20,the%20Zustand%20state%20management)), but often you can manage with external state alone.

We now have a solid approach to state: nodes and edges are managed in a central way. Next, we should consider **performance** implications as our app grows (lots of nodes, frequent updates) and how to optimize it.

## Performance Optimization

Building an advanced workflow editor means we need to keep the app **fast and responsive**, even as the number of nodes and interactions increases. React and React Flow are quite efficient, but there are best practices we should follow to avoid bottlenecks and unnecessary work.

Here are some performance optimization strategies:

- **Avoid Unnecessary Re-renders:** Utilize React’s memoization hooks and techniques. For instance, wrap components that don’t need to re-render on every state change in `React.memo` or `memo()` to prevent them from updating when their props haven’t changed. If we build custom node components, export them as `export default React.memo(MyNodeComponent)` so that they only render when their data/props change. This is important if you have many nodes: you don’t want all node components re-rendering just because one node changed. React Flow by default only re-renders nodes that have actually changed ([Introduction - React Flow](https://reactflow.dev/learn/concepts/introduction#:~:text=Customizable%3A%20React%20Flow%20supports%20custom,bespoke%20logic%20to%20node%20edges)), but if your node components do expensive work on render, memoization can help further.

- **useCallback and useMemo:** Use `useCallback` for event handlers or callbacks that you pass as props (like `onConnect`, custom handlers in nodes) to ensure they aren't recreated on every render unless dependencies change. This prevents child components from thinking props changed when they actually didn't (stable function references can keep `React.memo`ized children from re-rendering) ([Optimizing React Apps using useMemo and useCallback](https://getanteon.com/blog/optimizing-react-apps-using-usememo-and-usecallback/#:~:text=Here%2C%20,changes)) ([Optimizing React Apps using useMemo and useCallback](https://getanteon.com/blog/optimizing-react-apps-using-usememo-and-usecallback/#:~:text=Both%20useMemo%20and%20useCallback%20help,as%20props%20to%20child%20components)). Use `useMemo` for expensive calculations to cache results between renders ([Optimizing React Apps using useMemo and useCallback](https://getanteon.com/blog/optimizing-react-apps-using-usememo-and-usecallback/#:~:text=Without%20useMemo%2C%20the%20,useMemo%2C%20we%20can%20avoid%20this)) ([Optimizing React Apps using useMemo and useCallback](https://getanteon.com/blog/optimizing-react-apps-using-usememo-and-usecallback/#:~:text=Both%20useMemo%20and%20useCallback%20help,as%20props%20to%20child%20components)). For example, if you have a component that computes a layout or filters a large list of nodes, wrap that in useMemo so it re-computes only when necessary. However, remember that using these hooks has a small cost; apply them judiciously for cases where the saved work is significant ([Optimizing React Apps using useMemo and useCallback](https://getanteon.com/blog/optimizing-react-apps-using-usememo-and-usecallback/#:~:text=Both%20useMemo%20and%20useCallback%20help,as%20props%20to%20child%20components)) (don’t over-optimize trivial things).

- **Efficient State Updates:** When updating state, prefer batch updates or functional updates to avoid extraneous re-renders. In our store usage, for example, we used functional form `setNodes(nds => ...)` which React can batch if multiple updates happen in the same event loop. Also, avoid deeply nested state objects that trigger large re-renders; instead, normalize state (e.g., manage a map of node id to node data if needed, so updating one node is just updating one entry).

- **Large Graph Optimizations:** If your workflow might have hundreds of nodes, consider performance tips specific to React Flow:

  - Only render what’s needed. React Flow by default only renders visible nodes (it handles this internally), which is great. If you have custom renderings outside of React Flow, ensure you apply similar windowing/virtualization if dealing with large lists.
  - If doing expensive work on node position changes (like continuously updating some computation as a node is dragged), throttle or debounce those computations. For example, if you have an algorithm to update connected node positions or something on drag, use `lodash.throttle` or `requestAnimationFrame` to limit how often it runs.
  - If you experience slowdowns with a very large graph, consider toggling features like animations or shadows. Sometimes styling (like heavy box-shadows on hundreds of elements) can slow down the DOM; use simpler styles if needed for large counts.
  - Use web workers for extremely heavy computations. For instance, if you integrate an automatic layout algorithm (like DAGre or ElkJS for arranging the graph), those can be CPU-intensive. Running them in a web worker thread would keep the UI responsive.

- **Code Splitting:** This affects performance in terms of load time. As your app grows, using code splitting to load parts of the app only when needed can dramatically reduce initial load time ([Code-Splitting – React](https://legacy.reactjs.org/docs/code-splitting.html#:~:text=Code,needed%20during%20the%20initial%20load)). For example, if the workflow editor is just one part of a larger app, ensure that heavy libraries (like React Flow, DnD kit) are only loaded when the editor is actually used. In our case, if the editor is the main app, code splitting might not apply much (since we need all of it). But you could lazy-load rarely used components (maybe a settings panel or a large modal).

- **Bundle Size Management:** Monitor your bundle size. Material-UI and other libraries can add up. Use tools like webpack-bundle-analyzer or source-map-explorer to see what's contributing. Remove unused imports (tree-shaking usually does this) and consider using lighter alternatives if needed. For instance, if you only use a few icons from MUI Icons, you are already importing just those (since MUI Icons are exported individually). If using a lot, it’s fine, but always be mindful of large data or library imports.

- **Development vs Production Mode:** Always test performance with the production build. React in development has extra checks and warnings that make it slower. Make sure to build a minified production bundle (`npm run build`) and test that if you are benchmarking or noticing slowness ([Optimizing Performance - React](https://legacy.reactjs.org/docs/optimizing-performance.html#:~:text=If%20you%27re%20benchmarking%20or%20experiencing,with%20the%20minified%20production%20build)). The production build is much faster due to optimizations and removing debug overhead.

- **Memory leaks and long-running performance:** As users interact, ensure we clean up things. For example, if you add event listeners on window or timers (perhaps for auto-saving state periodically), clean them up on component unmount to avoid memory leaks. A memory leak can gradually degrade performance. Utilizing React’s useEffect cleanup or library-specific cleanup (like if we subscribe to React Flow’s internal store via `useStore`, clean up after if needed) is important.

- **Rendering large lists in side panels:** If we have a feature like a list of nodes or a log of actions, use virtualization (e.g., `react-window` or `react-virtualized`) for rendering long lists efficiently.

- **Profiling:** Use React’s Profiler API or the React Developer Tools Profiler to identify slow parts. This can highlight if a particular component is updating too often. For instance, you might discover your entire WorkflowPage re-renders when only one node changes – that might indicate you need to isolate state or wrap parts in `memo`. Profiling helps pinpoint these.

To illustrate, consider the use of `useMemo` and `useCallback`: if we have a compute-heavy formatting of node data:

```tsx
const formattedData = useMemo(() => expensiveFormat(nodes), [nodes]);
```

This ensures `expensiveFormat` runs only when `nodes` array changes, not on every render. And for callbacks:

```tsx
const handleNodeClick = useCallback(
  (nodeId: string) => {
    setSelectedNodeId(nodeId);
  },
  [setSelectedNodeId]
);
```

Now `handleNodeClick` can be passed to many nodes without re-allocating each time, and if those node components are memoized, they won't re-render unless the `handleNodeClick` reference changes (which it won't, due to useCallback, as long as setSelectedNodeId is stable).

One must balance optimization with complexity. As a rule of thumb: **optimize where a real issue exists** (after profiling or noticing lag), rather than pre-optimizing everything. Modern React is quite performant, and React Flow is built for performance, so many times things will just work well. When you do face performance issues, the above strategies will help mitigate them.

## Testing and Debugging

As we build this advanced application, ensuring reliability through testing and being able to debug issues is crucial. We'll discuss strategies for both **automated testing** (unit/integration tests) and **debugging techniques** during development.

### Testing the UI and Functionality

**1. Unit Testing Logic:** Parts of our application that are pure logic (not directly involving the browser DOM) should be unit tested. For example, if we have functions that manipulate the nodes list (like a function to delete a node or to validate a connection), we can write Jest tests for those. Similarly, if using Redux or context reducers, test the reducer functions for various action inputs. These tests ensure our state management logic is correct.

**2. Component Testing:** Using a tool like **React Testing Library (RTL)** with Jest allows us to render components in a simulated DOM and make assertions on their behavior. For instance, we can render our `<WorkflowPage>` (perhaps wrapping it in the necessary providers like ThemeProvider) and then simulate a drag-and-drop. However, simulating drag-and-drop in Jest/jsdom is tricky because jsdom doesn't implement the full drag-and-drop APIs realistically. You can somewhat simulate it by calling the event handlers (like calling `handleDragStart` then `onDrop` manually in the test with fabricated event objects), but that may not fully test the integration. Alternatively, we could use **React DnD Testing Library** or the utilities from react-testing-library to simulate dragging. There is also the possibility to mock the DnD kit behaviors.

For React Flow specifically, unit testing in Jest requires some mocks because React Flow relies on the DOM (ResizeObserver, etc.). The React Flow docs recommend using **Cypress or Playwright** for testing because they run in a real browser ([Testing - React Flow](https://reactflow.dev/learn/advanced-use/testing#:~:text=There%20are%20plenty%20of%20options,relies%20on%20rendering%20DOM%20elements)). If you use Jest, you need to mock certain global APIs (like `ResizeObserver` and `DOMMatrixReadOnly`) to prevent errors ([Testing - React Flow](https://reactflow.dev/learn/advanced-use/testing#:~:text=If%20you%20are%20using%20Jest%2C,will%20trigger%20the%20necessary%20overrides)). They even provide a snippet (`mockReactFlow()` as shown in their docs) to set up those mocks for Jest ([Testing - React Flow](https://reactflow.dev/learn/advanced-use/testing#:~:text=If%20you%20are%20using%20Jest%2C,will%20trigger%20the%20necessary%20overrides)). We would include that in a Jest setup file so that when our tests run, the environment is ready for ReactFlow components.

**3. Integration/E2E Testing:** Given the interactive nature (dragging, connecting nodes, etc.), end-to-end tests with a real browser are extremely valuable. **Cypress** and **Playwright** are two popular choices. With Cypress, for example, we can write a test that:

- Loads our application in a headless browser.
- Simulates a user dragging a "Task" item from the sidebar into the canvas (Cypress has commands for triggering drag events or you can use real mouse events).
- Asserts that a new node appears on the canvas with the correct label.
- Simulates connecting two nodes by dragging from one to the other.
- Asserts that an edge (line) is now present in the DOM connecting those nodes (you might check the SVG path element count increased, or some data attribute on edges if available).

Cypress will actually run the app, so no need for mocking DOM APIs – it uses a real browser environment, which aligns with React Flow's recommendation to use such tools ([Testing - React Flow](https://reactflow.dev/learn/advanced-use/testing#:~:text=There%20are%20plenty%20of%20options,relies%20on%20rendering%20DOM%20elements)).

**4. Testing Drag-and-Drop:** If using React DnD or DnD Kit, there are guides for writing tests. React DnD's docs have a section on testing with their TestBackend ([Testing - React DnD](https://react-dnd.github.io/react-dnd/docs/testing/#:~:text=Testing%20,libraries%2C%20like%20Jest%2C%20use)). For DnD kit, one could possibly simulate the DndContext events by triggering keyboard events or so, but it’s easier to rely on E2E tests to cover actual drag interactions. In Jest, an alternative is to factor out logic from the UI. For example, test that when `onDrop` is called with certain parameters, the `nodes` state updates correctly (you can call the store or context function and assert state). This is more of a unit test of the state logic rather than the drag UI.

**5. Snapshot Testing:** You can use snapshot tests for components to ensure UI doesn't change unexpectedly. For example, render a node component with given props and take a snapshot of the output HTML. This can catch accidental changes to the rendering of nodes or others. However, use this sparingly – snapshots of large components can become brittle if the UI changes often intentionally.

**6. Mocking modules:** In unit tests, you might mock parts of libraries if needed. For example, if a test doesn’t focus on drag-and-drop, you could mock `@dnd-kit/core` to noop to avoid dealing with it. Similarly, you could mock ReactFlow component in a unit test if you just want to test that your handlers are wired (though then you aren't testing the integration).

In summary, for testing:

- Use **Jest + RTL** for logic and simple component tests (with some mocking for React Flow).
- Use **Cypress/Playwright** for full user-flow testing (dragging, etc.) in a realistic environment, as these require no additional setup for DOM APIs ([Testing - React Flow](https://reactflow.dev/learn/advanced-use/testing#:~:text=Using%20Cypress%20or%20Playwright)).

### Debugging Techniques

Even with tests, during development you'll need to debug issues or verify behaviors:

- **Browser Developer Tools:** Use Chrome/Firefox DevTools to inspect the DOM, check styles (for instance, if a node isn't positioned where you expect, inspect its CSS or parent layout). Also use the Console to see any error messages. React Flow might warn about missing keys or ids conflicts there.

- **React Developer Tools:** Install the React DevTools extension for your browser. This allows you to inspect the React component tree in your app at runtime. You can verify the props and state of components. For example, you can select your `WorkflowPage` component and see what `nodes` and `edges` props (or context) it has. You can inspect a specific Node component (if you have custom ones) to see its data prop. This is extremely useful to debug state issues (like "why isn't my node data updating?").

- **Logging and Debug Statements:** It's often helpful to add temporary `console.log` statements. For instance, log inside `onDrop` to verify it's being called and what `nodeType` and position values are. Log the state length of nodes after adding to ensure it's updating. While you wouldn't keep these logs in production, during development they can quickly confirm behavior.

- **React Flow Devtools/Debugging:** The React Flow team has an experimental devtools package in progress ([Devtools and Debugging - React Flow](https://reactflow.dev/learn/advanced-use/devtools-and-debugging#:~:text=This%20is%20an%20ongoing%20experiment,com)). In lieu of that, they suggest techniques to log internal state: e.g., using `useReactFlow()` hook to get the instance and maybe log the current transform or using `onNodesChange` to log changes. They even provide example components like `<NodeInspector>` and `<ChangeLogger>` that you can mount in your app to output the current state ([Devtools and Debugging - React Flow](https://reactflow.dev/learn/advanced-use/devtools-and-debugging#:~:text=React%20Flow%20can%20often%20seem,internal%20state%20of%20your%20flow)). For example, a `<ChangeLogger>` could wrap your onNodesChange to log every node change event and the resulting state. These can be custom debug components you use during development to understand what's happening in the flow.

- **Using `useStore` from React Flow:** If needed, `useStore` (imported from 'reactflow') allows subscription to internal state. For example, `useStore(state => state.nodes)` would give you React Flow's internal node state. However, since we manage state externally, we might not use that. But if something seems off (like positions), you could cross-check what React Flow thinks the state is versus your external state.

- **Common Issues & Troubleshooting:**
  - If drag-and-drop isn’t working: Ensure the drag source (`draggable` attribute and onDragStart) is set correctly, and that `onDragOver` on the drop target is preventing default. If you forget `event.preventDefault()` on dragOver, the drop event might never fire ([Drag and Drop - React Flow](https://reactflow.dev/examples/interaction/drag-and-drop#:~:text=const%20onDragOver%20%3D%20useCallback%28%28event%29%20%3D,)).
  - If nodes aren’t appearing: Check that the React Flow container has a height > 0. A common issue is forgetting to set a style or height, resulting in a 0px tall canvas where nodes may actually be there but not visible. We set our container to 80vh as a quick fix; ensuring the parent flex container fills the screen as we did is important.
  - If new nodes all pile at {x:0,y:0}: That means our drop position calc might be wrong. Logging `reactFlowBounds` and event.clientX/Y can help adjust the formula.
  - If edges aren’t connecting: Check the node `type` and handle presence. React Flow by default gives 'source' handle on nodes of type 'output' and 'target' handle on type 'input'. If we used 'default' type for intermediate nodes, those have both source and target handles. We might need to adjust node types or provide custom handles to allow connections as desired. For debugging, turn on connection events: use `onConnectStart` and `onConnectEnd` to log when user starts/stops a connection drag.
  - If performance is slow with many nodes: Use the React Profiler (in React DevTools) to record while moving a node. It will show what components re-rendered and how long they took. Maybe you'll find, for example, that your entire sidebar re-rendered when moving a node – that would be a sign to isolate sidebar from context or wrap it in `React.memo` so it doesn’t re-render on node state changes (sidebar doesn’t need to update when nodes move).
- **Error Boundaries:** It might be wise to implement a React error boundary component around the Workflow editor, which can catch runtime errors (for example, if a custom node component throws an error). This prevents the whole app from crashing and could show a user-friendly message. During development, the error overlay will show you the stack trace, but in production an error boundary can log the error (maybe send to a logging service) and let the app continue running or prompt a reload.

- **DevTool Extensions:** If using Redux, obviously Redux DevTools are great for time-traveling through actions. For Zustand, you can use a devtools middleware to tie into Redux DevTools as well, which would let you see the history of state changes in the Chrome extension.

In practice, a combination of writing tests and using these debugging approaches will lead to a robust development process. Write tests for critical functionality (dragging creates nodes, connecting nodes adds edges, etc.), and use logging or devtools to investigate when something isn't working.

Remember to remove or disable verbose debug logs in production. Use environment variables or a logging utility that can be silenced in production builds to avoid cluttering the console or exposing internal info.

## Deployment and Best Practices

Having built and tested our Workflow UI application, the final step is deploying it and following best practices to ensure it runs smoothly in production. Let's discuss how to prepare the app for production deployment and some general best practices:

**1. Preparing for Production Build:**
When you're ready to deploy, run the production build command (for CRA, `npm run build`; for Vite, `npm run build` as well). This will compile and bundle our app into optimized static files. Create React App’s build script will minify the code, optimize assets, and produce a `build/` directory with HTML, JS, CSS files ready to serve ([Deployment of React Applications | Basic React | Chuck's Academy](https://www.chucksacademy.com/en/topic/react-basic/apps#:~:text=bash)). Ensure that no development-only code is running:

- If you have any `console.log` or `debugger` statements used during development, clean them up or wrap them in a check so they don't run in production.
- Make sure React is running in production mode (the build script sets `NODE_ENV=production` which strips out dev-only warnings and improves performance).

The result of the build is an **optimized bundle** – code is minified and the app is ready to serve efficiently ([Deployment of React Applications | Basic React | Chuck's Academy](https://www.chucksacademy.com/en/topic/react-basic/apps#:~:text=This%20command%20creates%20an%20optimized,to%20serve%20the%20application%20efficiently)).

**2. Hosting the Application:**
Our workflow editor is a single-page React app, which can be hosted on any static site hosting or served via any web server:

- **Static Hosting Services:** Netlify, Vercel, GitHub Pages, AWS S3/CloudFront, etc., are great for React apps. For example, you can drag-and-drop the `build/` folder to Netlify or use `git push` if connecting a repository. Netlify and Vercel can even auto-build your project from a Git repo – you just specify the build command and publish directory (e.g., `npm run build` and `build/` respectively) ([Deployment of React Applications | Basic React | Chuck's Academy](https://www.chucksacademy.com/en/topic/react-basic/apps#:~:text=1,main%20branch%20of%20your%20repository)) ([Deployment of React Applications | Basic React | Chuck's Academy](https://www.chucksacademy.com/en/topic/react-basic/apps#:~:text=,Publish%20Directory%3A%20%60build)).
- **Traditional Servers:** You can also serve the build with an Express.js server or any static file server. For instance, with Express:
  ```js
  app.use(express.static(path.join(__dirname, "build")));
  app.get("*", (req, res) => {
    res.sendFile(path.join(__dirname, "build", "index.html"));
  });
  ```
  This serves the static files and ensures all routes load `index.html` (since our app uses client-side routing if any).
- **Ensure correct base path:** If deploying to a sub-path (like `example.com/workflow/`), make sure to set the `homepage` in `package.json` for CRA or configure the base in Vite so that the build knows to reference assets correctly. Alternatively, handle it via the hosting configuration (e.g., setting correct base in Netlify).

**3. Environment Variables and Config:**
If your app needs configuration for production (like API endpoints, feature flags, etc.), use environment variables. For example, if connecting to a backend, you might have `REACT_APP_API_URL` for the API base. In production, set that variable (in Netlify/Vercel UI or a `.env.production` file) to the production API. This way the build embeds the correct URL. Never put secrets (like API keys for third-party services) in the front-end code unless absolutely necessary, and if you do, restrict their scope (e.g., use only public keys, as front-end code can be inspected by users).

**4. Performance Best Practices in Production:**

- **Caching:** Ensure that static assets are served with caching headers (most static hosts do this by default, giving long cache expiration for JS/CSS files since they include a hash in the filename). That way returning users load from cache.
- **CDN:** Use a CDN (Content Delivery Network) either via your host or manually to ensure fast global load times for the static files.
- **Monitoring Performance:** Consider using a performance monitoring tool (like Lighthouse CI, or services like New Relic, Datadog RUM, etc.) to catch if the app becomes slow in production or if there are any runtime errors happening for users.

**5. Application Best Practices:**

- **Documentation:** Document the code for future maintainers (or your future self). Complex parts like the drag-and-drop integration or the state structure should have comments or README notes explaining how they work. For instance, note that we rely on `dataTransfer` with `'application/reactflow'` MIME for DnD (someone reading the code might not immediately know why that string is used).

- **Error Handling:** Make the app resilient. Perhaps implement an **Error Boundary** around the main app to catch any uncaught errors and display a friendly message. For example, if a custom node component fails to render for some reason, an error boundary could catch it and prevent a blank screen. You might log the error to an error tracking service (like Sentry) for further analysis.

- **Accessibility (a11y):** Ensure the UI is accessible. This includes:
  - Keyboard support for all actions (React Flow has some built-in keyboard controls for selection and deletion; ensure those still work). Also, dragging with keyboard is a complex topic – DnD Kit actually has support for keyboard dragging (arrow keys to move items) ([Overview | @dnd-kit – Documentation](https://docs.dndkit.com/#:~:text=state%20management%20and%20context%2C%20which,keeps%20the%20library%20lean)). It might not fully apply to a canvas scenario, but consider providing alternative ways to add/move nodes (e.g., buttons to add node, properties to adjust position for those who can't drag).
  - Proper ARIA roles and labels: e.g., the sidebar list has role "list" via MUI’s List, and each item is a button, which is good. We might add `aria-grabbed` or other attributes when dragging for screen readers, but DnD kit handles some live region announcements if configured.
  - Color contrast: our color scheme should be checked (MUI's default theme generally is accessible, but if we customize colors, ensure sufficient contrast for text on backgrounds).
- **Security:** Since this is mostly front-end, security concerns are minimal, but still:

  - Keep dependencies updated for security patches. If using a backend API, ensure calls are over HTTPS and you properly handle tokens if any.
  - If the workflow can be saved, sanitize any data sent to backend.
  - Avoid eval or dynamic code execution in the front-end unless absolutely needed (if building something like a node that executes code, that's beyond our scope but be cautious).

- **State Persistence:** Decide if you want to persist the workflow state (e.g., if the page is reloaded, do we lose the workflow?). For a real app, you might implement a save feature (saving to server or localStorage). As a best practice, warn users if they might lose unsaved work (e.g., "Are you sure you want to leave? Unsaved workflow will be lost."). This can be done with the `beforeunload` event or React Router prompt if using routing.

- **Modularity and Reusability:** Perhaps wrap parts of functionality into custom hooks or utilities. For example, if some logic calculates positions or handles certain keyboard shortcuts, putting that in a hook (`useWorkflowShortcuts` for instance) could tidy up the main component and make it easier to maintain or test.

- **Continuous Integration/Deployment (CI/CD):** It's good practice to have automated builds and tests run on each commit. Use GitHub Actions or another CI service to run your test suite. Possibly integrate linters (ESLint) and type checking (tsc) as part of CI to ensure code quality. For deployment, CI can automatically deploy to a service like Netlify or Vercel on each push to main branch, which encourages iterative development and quick feedback.

- **Optimize Images/Assets:** If the app uses any images or heavy assets (our current design doesn't have much aside from maybe icons which are vector), ensure they're optimized (compressed, correct formats). Also use dynamic imports for large libraries if you only need them for some features (code splitting we discussed).

- **Monitoring and Logging in Production:** Include something to catch errors in production. For example, using `window.onerror` or a service like Sentry to log exceptions. This will help you know if users encounter issues after deployment.

- **User Experience Polishing:** Little things in a polished app:
  - Show a loading indicator if something is happening (e.g., if saving or loading workflows).
  - Provide confirmations for destructive actions (if you add a delete node feature, confirm it or allow undo).
  - Perhaps add tooltips to controls (MUI has Tooltip component).
  - Make the UI responsive (our layout is flex and should shrink, but might need tweaks for very small screens; maybe hide the sidebar behind a toggle on mobile).

Finally, a note on maintaining the application: as libraries update (React Flow often updates with improvements), keep an eye on changelogs for any breaking changes or new features you can take advantage of. For example, if a future version of React Flow offers a built-in way to handle external drag-and-drop, we might simplify our implementation using that.

Deploy the app, test it live on the URL, and interact with it as a user would. Ensure all features work in the production environment (sometimes environment differences can reveal new issues).

By following these practices, we ensure the Workflow UI application is **robust, performant, and maintainable** in the long run. From the initial architecture to deployment, we've covered the end-to-end process of building an advanced drag-and-drop workflow editor with React, TypeScript, React Flow, and Material-UI.

Good luck, and happy coding!

**Sources:**

- React Flow Documentation – _Introduction and Key Features_ ([Introduction - React Flow](https://reactflow.dev/learn/concepts/introduction#:~:text=React%20Flow%20is%20a%20library,controls%20out%20of%20the%20box)) ([Node-Based UIs in React - React Flow](https://reactflow.dev/#:~:text=Ready%20out))
- React Flow Documentation – _Drag and Drop Example_ ([Drag and Drop - React Flow](https://reactflow.dev/examples/interaction/drag-and-drop#:~:text=A%20drag%20and%20drop%20user,draggable)) ([Drag and Drop - React Flow](https://reactflow.dev/examples/interaction/drag-and-drop#:~:text=const%20position%20%3D%20screenToFlowPosition%28,type%7D%20node%60))
- Material-UI Documentation – _Overview_ ([Material UI: React components that implement Material Design](https://mui.com/material-ui/?srsltid=AfmBOopHf2hL9Ll6_Ul8Ds7scigiV894itvcwNA3GZPxtWIa23I1DqG7#:~:text=Material%20UI%20is%20an%20open,production%20out%20of%20the%20box)) ([Mastering Modern UI Development: A Comprehensive Guide to Using Material-UI with React - DEV Community](https://dev.to/christopherthai/mastering-modern-ui-development-a-comprehensive-guide-to-using-material-ui-with-react-9d6#:~:text=One%20of%20the%20standout%20features,to%20your%20brand%E2%80%99s%20unique%20aesthetic))
- DnD Kit Documentation – _Overview_ ([dnd kit – a modern drag and drop toolkit for React](https://dndkit.com/#:~:text=A%20lightweight%2C%20performant%2C%20accessible%20and,drop%20toolkit%20for%20React)) ([Overview | @dnd-kit – Documentation](https://docs.dndkit.com/#:~:text=,lists%2C%202D%20Games%2C%20and%20more))
- React Beautiful DnD – _Introduction_ ([Using React Beautiful DnD to Implement Drag and Drop](https://pieces.app/blog/implement-react-beautiful-dnd#:~:text=React%20Beautiful%20DnD%20is%20a,flexibility%20and%20offers%20many%20features)) ([Using React Beautiful DnD to Implement Drag and Drop](https://pieces.app/blog/implement-react-beautiful-dnd#:~:text=React%20Beautiful%20DnD%20is%20a,flexibility%20and%20offers%20many%20features))
- TypeScript vs JavaScript – _TypeScript definition_ ([TypeScript vs JavaScript - A Detailed Comparison | Refine](https://refine.dev/blog/javascript-vs-typescript/#:~:text=TypeScript%20is%20a%20statically%20typed,which%20JavaScript%20developers%20would%20find))
- Bulletproof React – _Project Structure guidelines_ ([bulletproof-react/docs/project-structure.md at master · alan2207/bulletproof-react · GitHub](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md#:~:text=For%20easy%20scalability%20and%20maintenance%2C,scalability%20in%20the%20application%27s%20architecture))
- Dev.to Article – _Container vs Presentational pattern_ ([Building Scalable React Applications: Design Patterns and Architecture - DEV Community](https://dev.to/drruvari/building-scalable-react-applications-design-patterns-and-architecture-39a0#:~:text=,UI%20based%20on%20props%20received))
- React Flow Docs – _State Management with Zustand_ ([Using a State Management Library - React Flow](https://reactflow.dev/learn/advanced-use/state-management#:~:text=As%20demonstrated%20in%20previous%20guides,as%20outlined%20in%20this%20guide)) ([Using a State Management Library - React Flow](https://reactflow.dev/learn/advanced-use/state-management#:~:text=library%20Zustand,as%20Redux%2C%20Recoil%20or%20Jotai))
- Anteon Blog – _useMemo and useCallback usage_ ([Optimizing React Apps using useMemo and useCallback](https://getanteon.com/blog/optimizing-react-apps-using-usememo-and-usecallback/#:~:text=Here%2C%20,changes)) ([Optimizing React Apps using useMemo and useCallback](https://getanteon.com/blog/optimizing-react-apps-using-usememo-and-usecallback/#:~:text=Both%20useMemo%20and%20useCallback%20help,as%20props%20to%20child%20components))
- React Flow Docs – _Testing recommendations_ ([Testing - React Flow](https://reactflow.dev/learn/advanced-use/testing#:~:text=There%20are%20plenty%20of%20options,relies%20on%20rendering%20DOM%20elements)) ([Testing - React Flow](https://reactflow.dev/learn/advanced-use/testing#:~:text=If%20you%20are%20using%20Jest%2C,will%20trigger%20the%20necessary%20overrides))
- Chuck's Academy – _Production Build Optimization_
