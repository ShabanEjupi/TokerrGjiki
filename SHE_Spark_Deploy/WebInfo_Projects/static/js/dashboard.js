/**
 * Dashboard JavaScript - Të gjitha funksionet e vizualizimit
 * Gjuha: Shqipe
 */

// Variablat globale
let currentTimeRange = 24;
let updateInterval;
let assetsData = [];

// Fillimi i dashboard-it
$(document).ready(function() {
    console.log('🚀 Duke nisur Dashboard-in Financiar...');
    
    // Ngarko të gjitha të dhënat
    loadAssets();
    updatePrices();
    updatePortfolio();
    updatePredictions();
    
    // Ngarko grafikun e parë automatikisht
    setTimeout(function() {
        if ($('#assetSelector option').length > 1) {
            $('#assetSelector').val($('#assetSelector option:eq(1)').val());
            updateChart();
            updateCandlestick();
        }
    }, 1000);
    
    // Përditësim automatik çdo 10 sekonda
    updateInterval = setInterval(function() {
        updatePrices();
    }, 10000);
});

// Ngarko listën e aseteve
function loadAssets() {
    $.get('/api/assets', function(assets) {
        assetsData = assets;
        
        // Popullo selector-ët
        let options = '<option value="">Zgjidh Asetin</option>';
        assets.forEach(function(asset) {
            options += `<option value="${asset.symbol}">${asset.name} (${asset.symbol})</option>`;
        });
        
        $('#assetSelector, #techAssetSelector, #volAssetSelector').html(options);
    });
}

// Ndërrimi i skedave
function showTab(tabName) {
    // Fshih të gjitha skedat
    $('.tab-content').hide();
    $('.tab').removeClass('active');
    
    // Shfaq skedën e zgjedhur
    $('#' + tabName + 'Tab').show();
    
    // Aktivizo butonin
    $('.tab').each(function() {
        const btnText = $(this).text().toLowerCase();
        if (btnText.includes(getTabWord(tabName))) {
            $(this).addClass('active');
        }
    });
    
    // Përditëso grafikët sipas skedës
    if (tabName === 'charts') {
        const asset = $('#assetSelector').val();
        if (asset) {
            updateChart();
            updateCandlestick();
        }
    } else if (tabName === 'technical') {
        const asset = $('#techAssetSelector').val();
        if (asset) {
            updateTechnical();
        }
    } else if (tabName === 'volume') {
        const asset = $('#volAssetSelector').val();
        if (asset) {
            updateVolume();
        }
        updateVolumeHeatmap();
    } else if (tabName === 'portfolio') {
        updatePortfolioChart();
    } else if (tabName === 'predictions') {
        updateConfidenceChart();
    }
}

function getTabWord(tabName) {
    const words = {
        'overview': 'përmbledhje',
        'charts': 'grafikët',
        'portfolio': 'portofoli',
        'predictions': 'parashikimet',
        'technical': 'teknikë',
        'volume': 'volumi'
    };
    return words[tabName] || tabName;
}

// Përditëso çmimet e drejtpërdrejta
function updatePrices() {
    $.get('/api/live-prices', function(data) {
        let html = '';
        
        for (let asset in data) {
            const assetData = data[asset];
            
            // Llogarit ndryshimin (mock për tani)
            const change = ((Math.random() - 0.5) * 5).toFixed(2);
            const changeClass = change > 0 ? 'positive' : change < 0 ? 'negative' : 'neutral';
            const changeSymbol = change > 0 ? '▲' : change < 0 ? '▼' : '•';
            const changePercent = `${changeSymbol} ${Math.abs(change)}%`;
            
            html += `
                <div class="asset-card" onclick="selectAsset('${asset}')">
                    <div class="asset-header">
                        <div>
                            <div class="asset-symbol">${asset}</div>
                            <div class="asset-name">${assetData.name}</div>
                        </div>
                        <div class="asset-change ${changeClass}">${changePercent}</div>
                    </div>
                    <div class="asset-price">$${assetData.price.toFixed(2)}</div>
                    <div class="asset-details">
                        <div>Lartë: $${assetData.high.toFixed(2)}</div>
                        <div>Ulët: $${assetData.low.toFixed(2)}</div>
                    </div>
                    <div style="margin-top: 10px; font-size: 11px; color: #8892b0;">
                        Volumi: ${formatNumber(assetData.volume)}
                    </div>
                </div>
            `;
        }
        
        $('#assetGrid').html(html);
        
        // Përditëso kohën e fundit
        const now = new Date();
        const options = { hour: '2-digit', minute: '2-digit', second: '2-digit' };
        $('#lastUpdate').text('Përditësuar: ' + now.toLocaleTimeString('sq-AL', options));
    }).fail(function() {
        console.error('Gabim në ngarkimin e çmimeve');
    });
}

// Zgjidh asetin dhe shfaq grafikun
function selectAsset(asset) {
    $('#assetSelector, #techAssetSelector, #volAssetSelector').val(asset);
    showTab('charts');
    updateChart();
    updateCandlestick();
}

// Përditëso grafikun e çmimeve
function updateChart() {
    const asset = $('#assetSelector').val();
    if (!asset) {
        console.log('Asnjë aset i zgjedhur për grafik');
        return;
    }
    
    console.log(`Duke ngarkuar grafikun për ${asset}...`);
    
    $.get(`/api/chart/${asset}?hours=${currentTimeRange}`, function(response) {
        console.log('Të dhënat e grafikut u ngarkuan:', response);
        
        const layout = response.layout;
        layout.height = 400;
        layout.margin = { l: 50, r: 50, t: 50, b: 50 };
        
        Plotly.newPlot('priceChart', response.data, layout, {
            responsive: true,
            displayModeBar: false
        });
        
        console.log('Grafiku u krijua me sukses!');
    }).fail(function(xhr, status, error) {
        console.error('Gabim në ngarkimin e grafikut:', error);
        console.error('Status:', status);
        console.error('Response:', xhr.responseText);
    });
}

// Përditëso grafikun candlestick
function updateCandlestick() {
    const asset = $('#assetSelector').val();
    if (!asset) return;
    
    $.get(`/api/candlestick/${asset}`, function(data) {
        const trace = {
            x: data.x,
            close: data.close,
            high: data.high,
            low: data.low,
            open: data.open,
            type: 'candlestick',
            name: 'Çmimi',
            increasing: {line: {color: '#00ff88'}},
            decreasing: {line: {color: '#ff3366'}}
        };
        
        const layout = {
            title: `Grafiku Candlestick - ${asset}`,
            xaxis: {title: 'Koha', gridcolor: '#2d3561'},
            yaxis: {title: 'Çmimi ($)', gridcolor: '#2d3561'},
            plot_bgcolor: '#1e2749',
            paper_bgcolor: '#1e2749',
            font: {color: '#ffffff'},
            height: 400,
            margin: { l: 50, r: 50, t: 50, b: 50 }
        };
        
        Plotly.newPlot('candlestickChart', [trace], layout, {
            responsive: true,
            displayModeBar: false
        });
    }).fail(function() {
        console.error('Gabim në ngarkimin e candlestick');
    });
}

// Vendos diapazonin kohor
function setTimeRange(hours) {
    currentTimeRange = hours;
    $('.chart-controls button').removeClass('active');
    event.target.classList.add('active');
    updateChart();
}

// Përditëso portofolet
function updatePortfolio() {
    $.get('/api/portfolio', function(data) {
        let html = '';
        
        for (let asset in data.allocation) {
            const alloc = data.allocation[asset];
            const percent = (alloc.weight * 100).toFixed(0);
            
            html += `
                <div class="allocation-item">
                    <div class="allocation-percent">${percent}%</div>
                    <div class="allocation-name">${alloc.name}</div>
                    <div style="font-size: 12px; color: #667eea; margin-top: 5px;">${alloc.reason}</div>
                    <div class="allocation-bar" style="width: ${percent}%"></div>
                </div>
            `;
        }
        
        $('#portfolioAllocation').html(html);
        
        // Përditëso metrikat
        $('#expectedReturn').text((data.metrics.expected_return * 100).toFixed(0) + '%');
        $('#sharpeRatio').text(data.metrics.sharpe_ratio.toFixed(2));
        $('#volatility').text((data.metrics.volatility * 100).toFixed(0) + '%');
    }).fail(function() {
        console.error('Gabim në ngarkimin e portofolit');
    });
}

// Përditëso grafikun e portofolit
function updatePortfolioChart() {
    $.get('/api/portfolio', function(data) {
        const labels = [];
        const values = [];
        
        for (let asset in data.allocation) {
            labels.push(data.allocation[asset].name);
            values.push(data.allocation[asset].weight);
        }
        
        const trace = {
            labels: labels,
            values: values,
            type: 'pie',
            marker: {
                colors: ['#00ff88', '#667eea', '#ff3366', '#ffaa00', '#00ccff', '#ff66cc', '#88ff00']
            },
            textinfo: 'label+percent',
            textfont: {color: '#ffffff', size: 14},
            hoverinfo: 'label+percent+value'
        };
        
        const layout = {
            title: 'Alokimi i Portofolit',
            plot_bgcolor: '#1e2749',
            paper_bgcolor: '#1e2749',
            font: {color: '#ffffff'},
            height: 500,
            showlegend: true,
            legend: {font: {color: '#ffffff'}}
        };
        
        Plotly.newPlot('portfolioChart', [trace], layout, {
            responsive: true,
            displayModeBar: false
        });
    });
}

// Përditëso parashikimet
function updatePredictions() {
    $.get('/api/predictions', function(data) {
        let html = '';
        
        for (let asset in data) {
            const pred = data[asset];
            const direction = pred.direction;
            const directionClass = direction === 'UP' ? 'positive' : direction === 'DOWN' ? 'negative' : 'neutral';
            const directionIcon = direction === 'UP' ? '📈' : direction === 'DOWN' ? '📉' : '➡️';
            const directionText = direction === 'UP' ? 'RRITJE' : direction === 'DOWN' ? 'RËNIE' : 'STABIL';
            
            // Badge për regjimin e tregut
            let regimeBadge = '';
            if (pred.market_regime) {
                const regime = pred.market_regime;
                let badgeColor = '#444';
                let regimeText = regime;
                
                if (regime.includes('Bull')) {
                    badgeColor = '#00ff88';
                    regimeText = 'Treg në Rritje';
                } else if (regime.includes('Bear')) {
                    badgeColor = '#ff3366';
                    regimeText = 'Treg në Rënie';
                } else if (regime.includes('Volatile')) {
                    badgeColor = '#ff9900';
                    regimeText = 'Volatilitet i Lartë';
                } else if (regime.includes('Stable')) {
                    badgeColor = '#4488ff';
                    regimeText = 'Treg i Qëndrueshëm';
                }
                
                regimeBadge = `<div style="background: ${badgeColor}; color: #0a192f; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; margin-top: 8px;">${regimeText}</div>`;
            }
            
            // Modelet individuale
            let modelsInfo = '';
            if (pred.models && Object.keys(pred.models).length > 0) {
                modelsInfo = '<div style="margin-top: 10px; font-size: 11px; color: #8892b0; text-align: left;">';
                modelsInfo += '<strong>Modelet:</strong><br>';
                for (let model in pred.models) {
                    const prob = (pred.models[model] * 100).toFixed(0);
                    const modelName = formatModelName(model);
                    modelsInfo += `${modelName}: ${prob}%<br>`;
                }
                modelsInfo += '</div>';
            }
            
            html += `
                <div class="asset-card">
                    <div class="asset-symbol">${asset}</div>
                    <div style="font-size: 48px; text-align: center; margin: 20px 0;">${directionIcon}</div>
                    <div class="asset-change ${directionClass}" style="text-align: center; width: 100%;">
                        ${directionText}
                    </div>
                    <div style="text-align: center; margin-top: 10px; color: #8892b0;">
                        <strong>Konfidenca: ${(pred.confidence * 100).toFixed(0)}%</strong>
                    </div>
                    <div style="text-align: center;">
                        ${regimeBadge}
                    </div>
                    ${modelsInfo}
                </div>
            `;
        }
        
        $('#predictionsGrid').html(html);
    }).fail(function() {
        console.error('Gabim në ngarkimin e parashikimeve');
    });
}

// Përditëso grafikun e konfidencës
function updateConfidenceChart() {
    $.get('/api/predictions', function(data) {
        const assets = [];
        const confidences = [];
        const colors = [];
        
        for (let asset in data) {
            assets.push(asset);
            confidences.push(data[asset].confidence * 100);
            
            // Ngjyra sipas drejtimit
            if (data[asset].direction === 'UP') {
                colors.push('#00ff88');
            } else if (data[asset].direction === 'DOWN') {
                colors.push('#ff3366');
            } else {
                colors.push('#667eea');
            }
        }
        
        const trace = {
            x: assets,
            y: confidences,
            type: 'bar',
            marker: {color: colors},
            text: confidences.map(c => c.toFixed(0) + '%'),
            textposition: 'outside',
            textfont: {color: '#ffffff'}
        };
        
        const layout = {
            title: 'Niveli i konfidencës për çdo aset',
            xaxis: {title: 'Aseti', gridcolor: '#2d3561'},
            yaxis: {title: 'Konfidenca (%)', gridcolor: '#2d3561', range: [0, 100]},
            plot_bgcolor: '#1e2749',
            paper_bgcolor: '#1e2749',
            font: {color: '#ffffff'},
            height: 400,
            margin: { l: 50, r: 50, t: 50, b: 100 }
        };
        
        Plotly.newPlot('confidenceChart', [trace], layout, {
            responsive: true,
            displayModeBar: false
        });
    });
}

// Përditëso treguesit teknikë
function updateTechnical() {
    const asset = $('#techAssetSelector').val();
    if (!asset) return;
    
    $.get(`/api/technical/${asset}`, function(data) {
        // RSI
        plotRSI(data.rsi);
        
        // Bollinger Bands
        plotBollingerBands(data.bollinger);
        
        // Mesataret Lëvizëse
        plotMovingAverages(data.moving_averages);
        
        // Momentumi
        plotMomentum(data.momentum);
        
        // Volatiliteti
        plotVolatility(data.volatility);
    }).fail(function() {
        console.error('Gabim në ngarkimin e treguesve teknikë');
    });
}

function plotRSI(data) {
    const trace1 = {
        x: data.x,
        y: data.y,
        type: 'scatter',
        mode: 'lines',
        name: 'RSI',
        line: {color: '#667eea', width: 2}
    };
    
    // Linjat 30 dhe 70
    const trace2 = {
        x: data.x,
        y: Array(data.x.length).fill(70),
        type: 'scatter',
        mode: 'lines',
        name: 'Mbiblerje (70)',
        line: {color: '#ff3366', width: 1, dash: 'dash'}
    };
    
    const trace3 = {
        x: data.x,
        y: Array(data.x.length).fill(30),
        type: 'scatter',
        mode: 'lines',
        name: 'Mbështyerje (30)',
        line: {color: '#00ff88', width: 1, dash: 'dash'}
    };
    
    const layout = {
        xaxis: {title: 'Koha', gridcolor: '#2d3561'},
        yaxis: {title: 'RSI', gridcolor: '#2d3561', range: [0, 100]},
        plot_bgcolor: '#1e2749',
        paper_bgcolor: '#1e2749',
        font: {color: '#ffffff'},
        height: 300,
        margin: { l: 50, r: 50, t: 20, b: 50 },
        showlegend: true,
        legend: {font: {color: '#ffffff', size: 10}}
    };
    
    Plotly.newPlot('rsiChart', [trace1, trace2, trace3], layout, {
        responsive: true,
        displayModeBar: false
    });
}

function plotBollingerBands(data) {
    const traces = [
        {
            x: data.x,
            y: data.upper,
            type: 'scatter',
            mode: 'lines',
            name: 'Brezi i Sipërm',
            line: {color: '#ff3366', width: 1}
        },
        {
            x: data.x,
            y: data.middle,
            type: 'scatter',
            mode: 'lines',
            name: 'Brezi i Mesëm',
            line: {color: '#667eea', width: 2}
        },
        {
            x: data.x,
            y: data.lower,
            type: 'scatter',
            mode: 'lines',
            name: 'Brezi i Poshtëm',
            line: {color: '#00ff88', width: 1}
        },
        {
            x: data.x,
            y: data.price,
            type: 'scatter',
            mode: 'lines',
            name: 'Çmimi',
            line: {color: '#ffffff', width: 2}
        }
    ];
    
    const layout = {
        xaxis: {title: 'Koha', gridcolor: '#2d3561'},
        yaxis: {title: 'Çmimi ($)', gridcolor: '#2d3561'},
        plot_bgcolor: '#1e2749',
        paper_bgcolor: '#1e2749',
        font: {color: '#ffffff'},
        height: 350,
        margin: { l: 50, r: 50, t: 20, b: 50 },
        showlegend: true,
        legend: {font: {color: '#ffffff', size: 10}}
    };
    
    Plotly.newPlot('bollingerChart', traces, layout, {
        responsive: true,
        displayModeBar: false
    });
}

function plotMovingAverages(data) {
    const traces = [
        {
            x: data.x,
            y: data.price,
            type: 'scatter',
            mode: 'lines',
            name: 'Çmimi',
            line: {color: '#ffffff', width: 2}
        },
        {
            x: data.x,
            y: data.ma5,
            type: 'scatter',
            mode: 'lines',
            name: 'MA 5',
            line: {color: '#00ff88', width: 1}
        },
        {
            x: data.x,
            y: data.ma14,
            type: 'scatter',
            mode: 'lines',
            name: 'MA 14',
            line: {color: '#667eea', width: 1}
        },
        {
            x: data.x,
            y: data.ma20,
            type: 'scatter',
            mode: 'lines',
            name: 'MA 20',
            line: {color: '#ff9900', width: 1}
        },
        {
            x: data.x,
            y: data.ma50,
            type: 'scatter',
            mode: 'lines',
            name: 'MA 50',
            line: {color: '#ff3366', width: 2}
        }
    ];
    
    const layout = {
        xaxis: {title: 'Koha', gridcolor: '#2d3561'},
        yaxis: {title: 'Çmimi ($)', gridcolor: '#2d3561'},
        plot_bgcolor: '#1e2749',
        paper_bgcolor: '#1e2749',
        font: {color: '#ffffff'},
        height: 350,
        margin: { l: 50, r: 50, t: 20, b: 50 },
        showlegend: true,
        legend: {font: {color: '#ffffff', size: 10}}
    };
    
    Plotly.newPlot('maChart', traces, layout, {
        responsive: true,
        displayModeBar: false
    });
}

function plotMomentum(data) {
    const traces = [
        {
            x: data.x,
            y: data.momentum7,
            type: 'scatter',
            mode: 'lines',
            name: 'Momentumi 7',
            line: {color: '#00ff88', width: 2}
        },
        {
            x: data.x,
            y: data.momentum14,
            type: 'scatter',
            mode: 'lines',
            name: 'Momentumi 14',
            line: {color: '#667eea', width: 2}
        }
    ];
    
    const layout = {
        xaxis: {title: 'Koha', gridcolor: '#2d3561'},
        yaxis: {title: 'Momentumi', gridcolor: '#2d3561'},
        plot_bgcolor: '#1e2749',
        paper_bgcolor: '#1e2749',
        font: {color: '#ffffff'},
        height: 300,
        margin: { l: 50, r: 50, t: 20, b: 50 },
        showlegend: true,
        legend: {font: {color: '#ffffff', size: 10}}
    };
    
    Plotly.newPlot('momentumChart', traces, layout, {
        responsive: true,
        displayModeBar: false
    });
}

function plotVolatility(data) {
    const traces = [
        {
            x: data.x,
            y: data.vol14,
            type: 'scatter',
            mode: 'lines',
            fill: 'tozeroy',
            name: 'Volatiliteti 14',
            line: {color: '#ff3366', width: 0},
            fillcolor: 'rgba(255, 51, 102, 0.3)'
        },
        {
            x: data.x,
            y: data.vol20,
            type: 'scatter',
            mode: 'lines',
            fill: 'tozeroy',
            name: 'Volatiliteti 20',
            line: {color: '#667eea', width: 0},
            fillcolor: 'rgba(102, 126, 234, 0.3)'
        }
    ];
    
    const layout = {
        xaxis: {title: 'Koha', gridcolor: '#2d3561'},
        yaxis: {title: 'Volatiliteti', gridcolor: '#2d3561'},
        plot_bgcolor: '#1e2749',
        paper_bgcolor: '#1e2749',
        font: {color: '#ffffff'},
        height: 300,
        margin: { l: 50, r: 50, t: 20, b: 50 },
        showlegend: true,
        legend: {font: {color: '#ffffff', size: 10}}
    };
    
    Plotly.newPlot('volatilityChart', traces, layout, {
        responsive: true,
        displayModeBar: false
    });
}

// Përditëso volumin
function updateVolume() {
    const asset = $('#volAssetSelector').val();
    if (!asset) return;
    
    $.get(`/api/volume/${asset}`, function(data) {
        // Grafiku i volumit dhe çmimit
        plotVolumePrice(data);
        
        // Përditëso statistikat
        $('#avgVolume').text(formatNumber(data.avg_volume));
        $('#maxVolume').text(formatNumber(data.max_volume));
        
        const trendText = data.trend > 0 ? `+${formatNumber(data.trend)}` : formatNumber(data.trend);
        const trendColor = data.trend > 0 ? '#00ff88' : data.trend < 0 ? '#ff3366' : '#667eea';
        $('#volumeTrend').text(trendText).css('color', trendColor);
    }).fail(function() {
        console.error('Gabim në ngarkimin e volumit');
    });
}

function plotVolumePrice(data) {
    const trace1 = {
        x: data.x,
        y: data.volume,
        type: 'bar',
        name: 'Volumi',
        marker: {color: '#667eea'},
        yaxis: 'y2'
    };
    
    const trace2 = {
        x: data.x,
        y: data.price,
        type: 'scatter',
        mode: 'lines',
        name: 'Çmimi',
        line: {color: '#00ff88', width: 2},
        yaxis: 'y1'
    };
    
    const layout = {
        xaxis: {title: 'Koha', gridcolor: '#2d3561'},
        yaxis: {
            title: 'Çmimi ($)',
            gridcolor: '#2d3561',
            side: 'left'
        },
        yaxis2: {
            title: 'Volumi',
            gridcolor: '#2d3561',
            side: 'right',
            overlaying: 'y'
        },
        plot_bgcolor: '#1e2749',
        paper_bgcolor: '#1e2749',
        font: {color: '#ffffff'},
        height: 400,
        margin: { l: 50, r: 50, t: 20, b: 50 },
        showlegend: true,
        legend: {font: {color: '#ffffff'}}
    };
    
    Plotly.newPlot('volumePriceChart', [trace1, trace2], layout, {
        responsive: true,
        displayModeBar: false
    });
}

// Përditëso heatmap e volumit
function updateVolumeHeatmap() {
    $.get('/api/volume-heatmap', function(data) {
        const trace = {
            x: data.assets,
            y: ['Volumi Mesatar'],
            z: [data.volumes],
            type: 'heatmap',
            colorscale: [
                [0, '#1e2749'],
                [0.5, '#667eea'],
                [1, '#00ff88']
            ],
            text: data.names,
            hovertemplate: '%{text}<br>Volumi: %{z:.0f}<extra></extra>'
        };
        
        const layout = {
            xaxis: {title: 'Aseti', gridcolor: '#2d3561'},
            yaxis: {gridcolor: '#2d3561'},
            plot_bgcolor: '#1e2749',
            paper_bgcolor: '#1e2749',
            font: {color: '#ffffff'},
            height: 200,
            margin: { l: 50, r: 50, t: 20, b: 100 }
        };
        
        Plotly.newPlot('volumeHeatmap', [trace], layout, {
            responsive: true,
            displayModeBar: false
        });
    }).fail(function() {
        console.error('Gabim në ngarkimin e heatmap');
    });
}

// Funksione ndihmëse
function formatNumber(num) {
    if (num >= 1e9) {
        return (num / 1e9).toFixed(2) + 'B';
    } else if (num >= 1e6) {
        return (num / 1e6).toFixed(2) + 'M';
    } else if (num >= 1e3) {
        return (num / 1e3).toFixed(2) + 'K';
    }
    return num.toFixed(0);
}

function formatModelName(model) {
    const names = {
        'random_forest': 'Pylli i Rastësishëm',
        'gradient_boosting': 'Gradient Boosting',
        'logistic_regression': 'Regresioni Logjistik',
        'svm': 'SVM'
    };
    return names[model] || model;
}
