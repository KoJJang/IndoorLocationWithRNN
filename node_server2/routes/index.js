module.exports = function(app, Wifi)
{
    // GET ALL BOOKS
    app.get('/api/wifis', function(req,res){
        Wifi.find(function(err, wifis){
            if(err) return res.status(500).send({error: 'database failure'});
            res.json(wifis);
        })
    });

    // GET BOOK BY AUTHOR
    app.get('/api/wifis/grid/:grid', function(req, res){
        Wifi.find({grid: req.params.grid},  function(err, wifis){
            if(err) return res.status(500).json({error: err});
            if(wifis.length === 0) return res.status(404).json({error: 'wifi not found'});
            res.json(wifis);
        })
    });

    app.post('/api/wifis', function(req, res){
        Wifi.findOne({bssid: req.body.bssid, grid: req.body.gridnum}, function(err, wifi){
            if(err) return res.status(500).json({error: err});
            if(!wifi){ // bssid랑 grid가 없는 경우
                var wifi = new Wifi();
                wifi.grid = req.body.gridnum;
                wifi.bssid = req.body.bssid;
                wifi.ssid = req.body.ssid;
                wifi.level.push(req.body.level);          
                wifi.save(function(err){
                    if(err){
                        console.error(err);
                        res.json({result: 0});
                        return;
                    }
                    res.json({result: 1});
                });
                return;
            }
            //bssid랑 grid가 있는경우
            wifi.level = wifi.level.concat([req.body.level]);
            wifi.save(function(err){
            if(err){
                console.error(err);
                res.json({result: 0});
                return;
            }
            res.json({result: 1});
            })
        });
    });

    app.post('/api/levels', function(req, res){
        console.log('who get in here post /users')
        var inputData = '';
        req.on('data',function(data){
            inputData = JSON.parse(data);
            console.log("levels: " + inputData.Level15);
        });
        req.on('end',function(){
            console.log("levels: " + inputData.Level15);
        });
        console.log("levels: " + inputData.Level15);
        console.log("request_body_levels: " + req.body.Level15);

        // if(err){
        //     console.error(err);
        //     res.json({result:0});
        //     res.write("BAD!");
        //     return;
        // }
        res.write("OK!");
        res.end();
    });
}
