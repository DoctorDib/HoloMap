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
import { RamStats, StateTypes } from '../../../../Interfaces/StateInterface';

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

const RamUsageDoughnutComponent = (): React.ReactElement => {
    const bytesToGB = (bytes: number, decimal: number = 1): string => {
        // 1 GB = 1024^3 bytes (or 2^30 bytes)
        return (bytes / (1024 ** 3)).toFixed(decimal);
    }

    const ram: RamStats = useSelector((state: StateTypes): StateTypes => state).root.heartbeat?.PcStats?.RamInfo;

    const options = {
        responsive: false,
        maintainAspectRatio: true,
        toolbar: {
            display: false,
        },
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: false,
                text: 'RAM Usage',
            },
        },
    };

    const data = {
        labels: [''],
        datasets: [
            {
                label: 'RAM Usage (%)',
                data: [ram?.PercentUsed, 100 - ram?.PercentUsed],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 99, 132, 0.5)'
                ],
                color: 'white',
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                ],
            },
        ],
    };

    return <>
        <div className={'stat-item'} style={{ width: '250px', height: '250px' }}>
            <div className={'chart'}>
                <Doughnut options={options} data={data} height={175} width={175}/>

                <div className={'center-container'}>
                    <div className={'title'}> RAM </div>
                    <div className={'value'}> {ram?.PercentUsed?.toFixed(1)}% </div>
                </div>
            </div>

            <div className={'info'} style={{ marginTop: 15, marginBottom: 0}}> Overall </div>
            <div className={'info'} style={{ marginTop: 0}}> {bytesToGB(ram?.Used)}GB / {bytesToGB(ram?.Total)}GB </div>
        </div>
    </>;
};

export default RamUsageDoughnutComponent;