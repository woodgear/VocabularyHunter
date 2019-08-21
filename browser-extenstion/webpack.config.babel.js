import path from "path";
import HtmlWebPackPlugin from "html-webpack-plugin";
import webpack from "webpack";
import MiniCssExtractPlugin from "mini-css-extract-plugin";
import CopyWebpackPlugin from 'copy-webpack-plugin';

const ASSET_PATH = process.env.ASSET_PATH || "./assert";
export default {
  entry: {
    // main:"./src/index.js",//后台主界面
    popup:"./src/components/page/popup/index.js",//工具栏弹窗
    background_script:"./src/background_script.js",//后台脚本
    content_script:"./src/content_script.js"//后台脚本
  },
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "[name].js",
  },
  devServer: {
    contentBase: path.join(__dirname, 'dist'),
    compress: false,
    port: 9000
  },
  plugins: [
    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // all options are optional
      filename: "[name].css",
      chunkFilename: "[id].css",
      ignoreOrder: false // Enable to remove warnings about conflicting order
    }),
    new HtmlWebPackPlugin({
      template: "./src/components/page/popup/index.html",
      filename: "popup.html",
    }),
    new CopyWebpackPlugin([
      {from:'assert/icons',to:'icons'},
      {from:'chrome-manifest.json',to:'manifest.json'},
  ]), 
  ],
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              // you can specify a publicPath here
              // by default it uses publicPath in webpackOptions.output
              publicPath: '../',
              hmr: process.env.NODE_ENV === 'development',
            },
          },
          'css-loader',
        ],
      },
      {
        test: /\.html$/,
        use: [
          {
            loader: "html-loader"
          }
        ]
      }
    ]
  }
};
