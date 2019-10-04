import path from "path";
import HtmlWebPackPlugin from "html-webpack-plugin";
import MiniCssExtractPlugin from "mini-css-extract-plugin";
import CopyWebpackPlugin from 'copy-webpack-plugin';
import  * as webpack from "webpack";

function defaultConfig() {
  return {
    entry: {
      popup: "./src/components/page/popup/index.js",//工具栏弹窗
      background_script: "./src/background_script.js",//后台脚本
      content_script: "./src/content_script.js",//后台脚本
      options: "./src/components/page/options/index.js",//配置界面
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
        filename: "[name].css",
        chunkFilename: "[id].css",
        ignoreOrder: false // Enable to remove warnings about conflicting order
      }),
      new HtmlWebPackPlugin({
        template: "./src/components/page/popup/index.html",
        filename: "popup.html",
        title: "popup",
        chunks: ["popup"],
        chunksSortMode: 'manual',
        inject: 'body'
      }),
      new HtmlWebPackPlugin({
        template: "./src/components/page/options/index.html",
        filename: "options.html",
        title: "options",
        chunks: ["options"],
        chunksSortMode: 'manual',
        inject: 'body'
      }),

      new CopyWebpackPlugin([
        { from: 'assert/icons', to: 'icons' },
        { from: 'chrome-manifest.json', to: 'manifest.json' },
      ]),
    ],
    module: {
      rules: [
        {
          test: /\.(jpg|png|gif|svg|pdf|ico)$/,
          use: [
              {
                  loader: 'file-loader',
                  options: {
                      name: '[path][name]-[hash:8].[ext]'
                  },
              },
          ]
      },
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
}

export default (env) => {
  console.log("start webpack", env)

  const devConfig = defaultConfig()
  devConfig.plugins.push(new CopyWebpackPlugin([
    { from: 'extenstion_config/config-dev.json', to: 'extenstion_config/config.json' },
  ]));

  if (env === "webpakc-dev-server") {
    const config = defaultConfig()
    config.plugins.push(new CopyWebpackPlugin([
      { from: 'extenstion_config/config-dev.json', to: 'extenstion_config/config.json' },
    ]));
    config.plugins.push(
      new webpack.NormalModuleReplacementPlugin(
        /browser_tool/,
        (resource)=>{
          console.log(resource.request)
          resource.request = resource.request.replace("browser_tool","mock_browser_tool");
        }
      ))
      return config;
  }

  if (env === "production") {
    console.log("production build")
    const config = defaultConfig();
    config.plugins.push(new CopyWebpackPlugin([
      { from: 'extenstion_config/config-product.json', to: 'extenstion_config/config.json' },
    ]));
    return config;

  } else if (env === "development") {
    console.log("development build")
    return devConfig;
  }
  console.log("development build")
  return devConfig;

}
