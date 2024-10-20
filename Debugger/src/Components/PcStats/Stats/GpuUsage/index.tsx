import React, { useEffect, useState } from 'react';
import { Bar, Doughnut } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from 'chart.js';

import '../../pcstats_style.scss';
import { useSelector } from 'react-redux';
import { GPUStat, StateTypes } from '../../../../Interfaces/StateInterface';

//https://react-chartjs-2-two.vercel.app/

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

const GpuUsageComponent = (): React.ReactElement => {
    const bytesToGB = (bytes: number, decimal: number = 1): string => {
        // 1 GB = 1024^3 bytes (or 2^30 bytes)
        return (bytes / (1024 ** 3)).toFixed(decimal);
    };

    const mbToGb = (mb: number) => (mb / 1024).toFixed(2); // 1 GB = 1024 MB

    const gpus: Array<GPUStat> = useSelector((state: StateTypes): StateTypes => state).root.heartbeat?.PcStats?.GpuInfo;

    return <>
        <div className={'stat-item'} style={{ width: '100%', height: '200px', justifyContent: 'flex-start', alignItems: 'center', overflowX: 'hidden', overflowY: 'scroll'  }}>

            {
                gpus?.map((gpu: GPUStat) => {
                    const barOptions = {
                        indexAxis: 'y' as const,
                        responsive: false,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: false,
                            },
                            title: {
                                text: gpu.Name,
                                display: true,
                                color: '#AE90BF',
                            },
                        },
                        scales: {
                            x: {
                                display: false,
                                min: 0,
                                max: gpu?.MemoryTotal,
                            },
                            y: {
                                ticks: {
                                    color: '#AE90BF',
                                },
                            },
                        },
                    };

                    const barData = {
                        labels: [`(${mbToGb(gpu.MemoryUsed)}GB / ${mbToGb(gpu.MemoryTotal)}GB)`],
                        datasets: [{ 
                            label: 'Memory Usage (MB)',
                            data: [gpu.MemoryUsed],
                            color: 'white',
                            backgroundColor: [
                                'rgba(54, 162, 235, 0.5)',
                            ],
                            borderColor: [
                                'rgba(54, 162, 235, 1)',
                            ],
                        }]
                    };

                    const barOptions2 = {
                        indexAxis: 'y' as const,
                        responsive: false,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: false,
                            },
                            title: {
                                display: false,
                            },
                        },
                        scales: {
                            x: {
                                display: false,
                                min: 0,
                                max: 85,
                            },
                            y: {
                                ticks: {
                                    color: '#AE90BF',
                                },
                            },
                        },
                    };

                    const barData2 = {
                        labels: ['Temperature'],
                        datasets: [{
                            label: 'Temperature (c)',
                            data: [gpu.Temperature],
                            color: 'white',
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.5)',
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                            ],
                        }]
                    };

                    return (
                        <div style={{ flexDirection: 'row', width: '100%', borderBottom: '1px solid black' }}>
                            {/* <div className={'title'}> {gpu.Name} </div> */}
                            <div className={'chart'} >
                                <Bar options={barOptions} data={barData} height={75} width={250} />    
                                <Bar options={barOptions2} data={barData2} height={50} width={250} />                            
                            </div>
                        </div>
                    );
                })
            }
            
        </div>
    </>;
};

export default GpuUsageComponent;