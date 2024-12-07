import { Module, Modules } from "../../Interfaces/StateInterface";

const buildTree = (moduleObject: Modules): [Module[], Modules] => {

    const modules = Object.values(moduleObject);

    // Create a mapping of module names to their details
    const moduleMap: Modules = {};

    Object.values(modules).forEach((module: Module) => {
        moduleMap[module.Name] = { ...module, Children: [] };
    });
  
    // Initialize the roots of the tree
    const roots: Module[] = [];

    // Build the tree structure
    modules.forEach((module) => {
        const parentName = module.ModuleParentName;
        const name = module.Name;
    
        if (parentName === null || parentName === "") {
          // If no parent, add it as a root
          roots.push(moduleMap[name]);
        } else {
            // If a parent exists, add it as a child
            const parent = moduleMap[parentName];
            
              if (parent) {
                parent.Children?.push(moduleMap[name]);
            } else {
                // Handle the case where the parent is not found (optional)
                console.warn(`Warning: Parent ${parentName} not found for module ${name}`);
            }
        }
    });

    return [roots, moduleMap];
}

export default buildTree;