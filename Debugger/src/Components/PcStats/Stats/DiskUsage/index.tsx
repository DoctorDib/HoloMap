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
import { DiskStats, RamStats, StateTypes } from '../../../../Interfaces/StateInterface';

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

const DiskUsageComponent = (): React.ReactElement => {
    const bytesToGB = (bytes: number, decimal: number = 1): string => {
        // 1 GB = 1024^3 bytes (or 2^30 bytes)
        return (bytes / (1024 ** 3)).toFixed(decimal);
    }

    const disk: Array<DiskStats> = useSelector((state: StateTypes): StateTypes => state).root.heartbeat?.PcStats?.DiskInfo;

    const barOptions = {
        indexAxis: 'y' as const,
        responsive: false,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                text: "Disk Space",
                display: true,
                color: '#AE90BF',
            },
        },
        scales: {
            x: {
                display: false,
                min: 0,
                max: 100,
            },
            y: {
                ticks: {
                    color: '#AE90BF',
                }
            }
        },
    };

    const barData = {
        labels: disk?.map((disk: DiskStats) => `${disk?.Device} (${bytesToGB(disk?.Usage?.Used)} / ${bytesToGB(disk?.Usage?.Total)})`),
        datasets: [
            {
                label: 'Disk Usage (%)',
                data: disk?.map((disk: DiskStats) => disk?.Usage?.PercentUsed),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                ],
            },
        ],
    };

    useEffect(() => {
        console.log(disk?.map((disk: DiskStats) => disk?.Usage?.PercentUsed))
    }, [disk]);

    return <>
        <div className={'stat-item'} style={{ width: '200px', height: '200px' }}>
            <div className={'chart'}>
                <Bar options={barOptions} data={barData} height={200} />
            </div>

            {/* <div className={'info'} style={{ marginTop: 15, marginBottom: 0}}> Overall </div>
            <div className={'info'} style={{ marginTop: 0}}> {bytesToGB(ram?.Used)}GB / {bytesToGB(ram?.Total)}GB </div> */}
            
        </div>
    </>;
};

export default DiskUsageComponent;