Collecting workspace information```markdown
# The Planner's Assistant – Frontend

This is the frontend for **The Planner's Assistant**, a modern web application designed to support local plan production and development management workflows for planning authorities. Built with [SvelteKit](https://kit.svelte.dev/), [TypeScript](https://www.typescriptlang.org/), and [Tailwind CSS](https://tailwindcss.com/), it provides interactive tools for policy drafting, site allocation, scenario analysis, and development management casework.

---

## Features

- **Plan Production Workspace**
  - **Policy Tools:** Draft, edit, and analyze planning policies.
  - **Site Allocation:** Manage and justify site allocations with policy and constraint context.
  - **Scenario Analysis:** Compare alternative plan scenarios, track goal performance, and visualize trade-offs.
  - **Goal Tracker:** Monitor strategic goals, their status, and cross-cutting insights.
  - **Document Editor:** Structure and edit plan documents with integrity checks and export options.

- **Development Management Workspace**
  - **Site Assessment:** Assess planning applications and sites against constraints and policies.
  - **Reasoning Mode:** Step through application reasoning, link policies, and analyze trade-offs.
  - **Precedent Review:** Browse and compare relevant case precedents.
  - **Report Generation:** Draft and export officer reports with supporting evidence.

- **Dashboard**
  - Quick access to recent applications, plan production tools, and current projects.

---

## Project Structure

```
frontend/
├── src/
│   ├── app.css                # Tailwind CSS entry
│   ├── app.html               # HTML template
│   ├── lib/
│   │   ├── components/        # Svelte components (policy, site, scenario, goal, document, etc.)
│   │   ├── services/          # Data/mock services
│   │   ├── stores/            # Svelte stores for app state
│   │   └── types/             # TypeScript models and types
│   ├── routes/                # SvelteKit routes (pages)
│   │   ├── +layout.svelte     # Main layout and navigation
│   │   ├── +layout.ts         # Workspace/mode loader
│   │   └── ...                # Workspace and mode pages
│   └── static/                # Static assets (favicon, etc.)
├── tailwind.config.cjs        # Tailwind CSS config
├── postcss.config.cjs         # PostCSS config
├── svelte.config.js           # SvelteKit config
├── tsconfig.json              # TypeScript config
├── package.json               # NPM scripts and dependencies
└── README.md                  # This file
```

---

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v18+ recommended)
- [npm](https://www.npmjs.com/) or [pnpm](https://pnpm.io/)

### Installation

```sh
cd frontend
npm install
```

### Development

Start the development server:

```sh
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) (or as indicated in the terminal) in your browser.

### Build for Production

```sh
npm run build
```

Preview the production build:

```sh
npm run preview
```

### Linting & Formatting

- **Lint:**  
  `npm run lint`
- **Format:**  
  `npm run format`
- **Type Check:**  
  `npm run check`

---

## Key Technologies

- **[SvelteKit](https://kit.svelte.dev/):** Modern, fast web framework for building interactive apps.
- **[TypeScript](https://www.typescriptlang.org/):** Type-safe JavaScript.
- **[Tailwind CSS](https://tailwindcss.com/):** Utility-first CSS framework.
- **[Leaflet](https://leafletjs.com/):** Interactive maps for site and constraint visualization.

---

## Folder Highlights

- [`src/lib/components/`](src/lib/components/):  
  Modular Svelte components for each workspace and panel.

- [`src/lib/types/models.ts`](src/lib/types/models.ts):  
  Central TypeScript types for policies, sites, scenarios, goals, applications, etc.

- [`src/lib/stores/mainDataStore.ts`](src/lib/stores/mainDataStore.ts):  
  Svelte stores for managing application state and mock data.

- [`src/routes/`](src/routes/):  
  SvelteKit pages for each workspace and mode.

---

## Customization

- **Tailwind Theme:**  
  Custom colors and typography are defined in [`tailwind.config.cjs`](tailwind.config.cjs).

- **Workspace & Mode Navigation:**  
  Workspace and mode definitions are managed in [`src/routes/+layout.svelte`](src/routes/+layout.svelte) and [`src/routes/+layout.ts`](src/routes/+layout.ts).

- **Mock Data:**  
  The app uses mock data/services for demonstration. See [`src/lib/services/mockData.ts`](src/lib/services/mockData.ts).

---

## License

This project is licensed under the GNU Affero General Public License v3.0. See [LICENSE](../LICENSE) for details.

---

## Contact

For questions or contributions, please open an issue or pull request on the repository.