import React from 'react';
import { Bar, Doughnut } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
} from 'chart.js';

import '../../pcstats_style.scss';
import { useSelector } from 'react-redux';
import { CpuStats, StateTypes } from '../../../../Interfaces/StateInterface';

//https://react-chartjs-2-two.vercel.app/

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
);

const CpuUsageDoughnutComponent = (): React.ReactElement => {

    const cpu: CpuStats = useSelector((state: StateTypes): StateTypes => state).root.heartbeat?.PcStats?.CpuInfo;

    const doughnutOptions = {
        responsive: false,
        maintainAspectRatio: false,
        toolbar: {
            display: false,
        },
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: false,
                text: 'CPU Usage',
            },
        },
    };

    const doughnutData = {
        labels: [''],
        datasets: [
            {
                label: 'CPU Usage (%)',
                data: [cpu?.CpuUsage, 100 - cpu?.CpuUsage],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 99, 132, 0.5)',
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                ],
            },
        ],
    };

    const barOptions = {
        indexAxis: 'y' as const,
        responsive: true,
        maintainAspectRatio: true,
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
                max: 100,
            }
        },
    };

    const barData = {
        labels: cpu?.CpuUsagePerCore.map((_: string, index: number) => `${index  +1}`),
        datasets: [
            {
                label: 'CPU Usage (%)',
                data: cpu?.CpuUsagePerCore.map((usage: string) => parseFloat(usage.replace('%', ''))),
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

    return <>
        <div className={'stat-item'} style={{ width: '250px', height: '250px' }}>

            <div className={'chart'}>
                <Doughnut options={doughnutOptions} data={doughnutData} height={165} />

                <div className={'center-container'}>
                    <div className={'title'}> CPU </div>
                    <div className={'value'}> {cpu?.CpuUsage.toFixed(1)}% </div>
                </div>
            </div>

            <div className={'info'} style={{ marginTop: 15, marginBottom: 0}}> CPU Cores </div>
            <Bar options={barOptions} data={barData} height={125}/>
        </div>
    </>;
};

export default CpuUsageDoughnutComponent;