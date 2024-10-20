module.exports = {
    root: true,
    parser: '@typescript-eslint/parser',
    parserOptions: {
        tsconfigRootDir: __dirname,
        project: ['./tsconfig.json'],
        ecmaVersion: 2020,
        ecmaFeatures: {
            jsx: true,
        },
    },
    plugins: [
        '@typescript-eslint',
    ],
    extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'airbnb-typescript',
        'plugin:import/errors',
        'plugin:import/warnings',
        'plugin:import/typescript',
        "plugin:react/recommended",
        "plugin:react-hooks/recommended",
    ],
    rules: {
        
        'react-hooks/exhaustive-deps': 'warn',
        "react/jsx-uses-react": "off",
        "react/react-in-jsx-scope": "off",
        "linebreak-style": 0,
        "indent": "off",
        "@typescript-eslint/indent": ["error", 4],
        "react/jsx-indent-props": 0,
        "react/jsx-indent": 0,
        "react/require-default-props": 0,
        "react/no-unused-prop-types": 0,
        "@typescript-eslint/no-empty-interface": 0,
        // these two are because eslint hates me
        "no-use-before-define": 0,
        "@typescript-eslint/no-use-before-define": 0,
        "max-len": ["error", { 
            "code": 150,
            "ignoreComments": true,
            "ignoreStrings": true,

        }],
        "no-console": 0,
        "no-plusplus": ["warn", {
            "allowForLoopAfterthoughts": true,
        }],
        "no-continue": 0,
        "object-curly-newline": 0,
        "implicit-arrow-linebreak": 0,
        "react/jsx-props-no-spreading": 0,
        "arrow-spacing": "error",
        "import/no-extraneous-dependencies": [
            "error", {
               "devDependencies": false, 
               "optionalDependencies": false, 
               "peerDependencies": false, 
               "packageDir": "./"
            }
        ],
        // "import/no-extraneous-dependencies": ["error", {"devDependencies": true}],
        "@typescript-eslint/no-inferrable-types": "warn",
        "react/prop-types": "off",
    },
    env: {
        "browser": true,
        "node": true,
        "commonjs": true,
    },
    settings: {
        react: {
            version: 'detect',
        },
    },
    globals: {
        // https://stackoverflow.com/questions/34820817/eslints-no-undef-rule-is-calling-my-use-of-underscore-an-undefined-variable
        // Preventing error when we're using ReactCrop namespace from node_modules
        "ReactCrop": false,
    },
};