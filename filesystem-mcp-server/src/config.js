import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const defaultRoot = path.resolve(__dirname, "..", "..");

export const repositoriesRoot = path.resolve(
  process.env.REPOSITORIES_ROOT || defaultRoot
);
