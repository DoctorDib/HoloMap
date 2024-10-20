// import webpack from 'webpack';

// export default {
//     module: {
//         rules: [
//             {
//                 test: /\.tsx?$/, // Test for .ts or .tsx files
//                 use: 'ts-loader', // Use 'ts-loader'
//                 exclude: /node_modules/, // Exclude node_modules folder
//             },
//             {
//                 test: /\.js$/, // Test for .js files
//                 enforce: 'pre', // Make sure this loader runs before others
//                 use: 'source-map-loader', // Use 'source-map-loader'
//                 exclude: /node_modules/, // Exclude node_modules folder
//             },
//         ],
//     },
//     resolve: {
//         extensions: ['.ts', '.tsx', '.js'], // Resolve these extensions
//         fallback: {
//             path: require.resolve('path-browserify'), // Polyfill for 'path'
//             process: require.resolve('process/browser'), // Polyfill for 'process'
//         },
//     },
//     plugins: [
//         new Dotenv(), // Add this line
//         new webpack.DefinePlugin({
//             'process.env': JSON.stringify(env), // Inject environment variables
//         }),
//     ],
// };
