const path = require('path');
// const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const webpack = require('webpack');
// const WebpackDashDynamicImport = require('@plotly/webpack-dash-dynamic-import');
const packagejson = require('./package.json');

const dashLibraryName = packagejson.name.replace(/-/g, '_');

module.exports = (env, argv) => {

    let mode;

    const overrides = module.exports || {};

    // if user specified mode flag take that value
    if (argv && argv.mode) {
        mode = argv.mode;
    }

    // else if configuration object is already set (module.exports) use that value
    else if (overrides.mode) {
        mode = overrides.mode;
    }

    // else take webpack default (production)
    else {
        mode = 'production';
    }

    let filename = (overrides.output || {}).filename;
    if (!filename) {
        const modeSuffix = mode === 'development' ? 'dev' : 'min';
        filename = `${dashLibraryName}.${modeSuffix}.js`;
    }

    const entry = overrides.entry || {main: './src/lib/index.js'};

    const devtool = overrides.devtool || 'source-map';

    const externals = ('externals' in overrides) ? overrides.externals : ({
        react: 'React',
        'react-dom': 'ReactDOM',
        'plotly.js': 'Plotly',
        'prop-types': 'PropTypes',
    });

    return {
        mode: mode,
        entry,
        output: {
            path: path.resolve(__dirname, dashLibraryName),
            chunkFilename: '[name].chunk.js',
            filename,
            library: dashLibraryName,
            libraryTarget: 'window',
        },
        devtool,
        externals: externals,
        module: {
            rules: [
                {
                    test: /\.jsx?$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                    },
                },
                {
                    test: /\.s[ac]ss$/i,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader,
                        },
                        {
                            loader: 'css-loader',
                            options: {
                                sourceMap: true,
                            },
                        },
                        {
                            loader: 'sass-loader',
                            options: {
                                implementation: require("sass"),
                                sourceMap: true,
                            }
                        },
                    ],
                },
                {
                    test: /\.css$/i,
                    use: [
                        {
                            loader: MiniCssExtractPlugin.loader,
                        },
                        {
                            loader: 'css-loader',
                        },
                    ],
                },
                {
                    test: /\.(woff(2)?)(\?v=\d+\.\d+\.\d+)?$/,
                    use: [
                        {
                            loader: 'url-loader',
                            options: {
                                limit: 10000,
                                mimetype: 'application/font-woff',
                                outputPath: '../../assets/fonts',
                                publicPath: '/assets/fonts',
                            }
                        },
                    ],
                },
                {
                    test: /\.(eot|svg|ttf)(\?v=\d+\.\d+\.\d+)?$/,
                    use: [
                        {
                            loader: 'file-loader',
                            options: {
                                outputPath: '../../assets/fonts',
                                publicPath: '/assets/fonts',
                            }
                        },
                    ],
                },
            ],
        },
        optimization: {
            minimizer: [
                new TerserPlugin({
                    sourceMap: true,
                    parallel: true,
                    cache: './.build_cache/terser',
                    terserOptions: {
                        warnings: false,
                        ie8: false
                    }
                })
            ],
            splitChunks: {
                name: false,
                cacheGroups: {
                    async: {
                        chunks: 'async',
                        minSize: 0,
                        name(module, chunks, cacheGroupKey) {
                            return `${cacheGroupKey}-${chunks[0].name}`;
                        }
                    },
                    shared: {
                        chunks: 'all',
                        minSize: 0,
                        minChunks: 2,
                        name: 'test_runner_components-shared'
                    }
                }
            }
        },
        plugins: [
            // new WebpackDashDynamicImport(),
            new webpack.SourceMapDevToolPlugin({
                filename: '[file].map',
                exclude: ['async-plotlyjs']
            }),
            new MiniCssExtractPlugin({
                filename: '../../assets/style.css',
            }),
            //           new HtmlWebpackPlugin(Object.assign({
            //               filename: 'index.html'
            //           }, {
            //               inject: true,
            //               hash: true,
            //               template: path.join(__dirname, '/src/lib/index.ejs'),
            //           })),
            // new HtmlWebpackPlugin({
            //    inject: true,
            //    hash: true,
            //    template: './src/lib/index.ejs',
            //    filename: 'index.html'
            // }),
        ]
    }
};
