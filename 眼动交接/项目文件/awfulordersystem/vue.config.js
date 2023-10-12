// An highlighted block
module.exports = {
    devServer: {
        port: 8080, //前端接口
        proxy: {
            '/api': {//代理api
                target: "http://localhost:5000",// 代理接口(注意只要域名就够了)
                changeOrigin: true,//是否跨域
                ws: true, // proxy websockets
                pathRewrite: {//重写路径
                    "^/api": ''//代理路径
                }
            }
        }
    }
}
