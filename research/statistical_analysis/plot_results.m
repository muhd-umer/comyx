% Define data
clear;
close all;
set(groot,'defaulttextinterpreter','latex');
set(groot, 'defaultLegendInterpreter','latex');
set(groot, 'defaultAxesTickLabelInterpreter','latex');
set(groot,'defaultLineMarkerSize', 6);
Pt = load(".\results\tx_power_dB.mat").tx_power;

%% Outage
ris = load(".\results\results_ris34.mat");
noris = load(".\results\results_no_ris.mat");
noris_nocomp = load(".\results\results_no_ris_non_comp.mat");

fig1 = figure();

% RIS K = 32 Elements
semilogy(Pt, ris.outage(1, :), 'LineWidth', 1.5, ...
    'LineStyle', '-' ,'Color', 'black');
hold on;
semilogy(Pt, ris.outage(2, :), 'LineWidth', 1.5, ....
    'LineStyle', '--', 'Color', 'black');
semilogy(Pt, ris.outage(5, :), 'LineWidth', 1.5, ...
    'LineStyle', '-.', 'Color', 'black');
% semilogy(Pt, noris.outage(1, :), 'LineWidth', 1.5, ...
%     'LineStyle', '-', 'Color', 'red');
% semilogy(Pt, noris.outage(2, :), 'LineWidth', 1.5, ...
%     'LineStyle', '-', 'Color', 'red');
semilogy(Pt, noris.outage(3, :), 'LineWidth', 2, ...
    'LineStyle', ':', 'Color', 'black');
semilogy(Pt, noris_nocomp.outage(1, :), 'LineWidth', 2, ...
    'LineStyle', '--', 'Color', 'black');
p1 = semilogy(Pt, ris.outage(3, :), 'LineStyle', 'none', ...
    'LineWidth', 1.5, 'Marker', 'x', 'MarkerIndices', ...
    1:5:length(Pt), 'Color', 'red');
p1.MarkerSize = 8.5;
semilogy(Pt, ris.outage(4, :), 'LineStyle', 'none', ...
    'LineWidth', 1.5, 'Marker', 'o', 'MarkerIndices', ...
    1:5:length(Pt), 'Color', 'red');
semilogy(Pt, ris.outage(6, :), 'LineStyle', 'none', ...
    'LineWidth', 1.5, 'Marker', 's', 'MarkerIndices', ...
    1:5:length(Pt), 'Color', 'red');
% p1 = semilogy(Pt, noris.outage(4, :), 'LineStyle', 'none', ...
%     'LineWidth', 1.5, 'Marker', 's', 'MarkerIndices', ...
%     1:5:length(Pt), 'Color', 'black');
% p1.MarkerFaceColor = p1.Color;
% p2 = semilogy(Pt, noris.outage(5, :), 'LineStyle', 'none', ...
%     'LineWidth', 1.5, 'Marker', 'd', 'MarkerIndices', ...
%     1:5:length(Pt), 'Color', 'black');
% p2.MarkerFaceColor = p2.Color;
p3 = semilogy(Pt, noris.outage(6, :), 'LineStyle', 'none', ...
    'LineWidth', 1.5, 'Marker', '^', 'MarkerIndices', ...
    1:5:length(Pt), 'Color', 'red');
% p3.MarkerFaceColor = p3.Color;
p4 = semilogy(Pt, noris_nocomp.outage(2, :), 'LineStyle', 'none', ...
    'LineWidth', 1.5, 'Marker', '*', 'MarkerIndices', ...
    1:5:length(Pt), 'Color', 'red');
% p4.MarkerFaceColor = p4.Color;
p4.MarkerSize = 7;

% Add labels and legend
xlabel('Transmit power per BS, $P_t$ (dBm)');
ylim([9e-4 1])
xlim([-40 0])
ylabel('Outage probability');
x1 = 24.5;
x2 = 18;
leg = legend('Analytical, U$_{1,c}$, {$K$ = 34} Elements', ...
    'Analytical, U$_{2,c}$, {$K$ = 34} Elements', ...
    'Analytical, U$_{f}$, {$K$ = 34} Elements', ...
    'Analytical, U$_{f}$, without RIS', ...
    'Analytical, U$_{f}$, Non-CoMP, without RIS', ...
    'Simulation, U$_{1,c}$, {$K$ = 34} Elements', ...
    'Simulation, U$_{2,c}$, {$K$ = 34} Elements', ...
    'Simulation, U$_{f}$, {$K$ = 34} Elements', ...
    'Simulation, U$_{f}$, without RIS', ...
    'Simulation, U$_{f}$, Non-CoMP, without RIS', ...
    'Location', 'southwest', 'FontSize', 10);
leg.ItemTokenSize = [x1, x2];
leg.FontSize = 9;

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% Sum-rate
no_ris = load(".\results\results_no_ris.mat");
ris32 = load(".\results\results_ris32.mat");
ris70 = load(".\results\results_ris70.mat");
custom = load(".\results\results_ris70_oPA.mat");

fig5 = figure();

% Plot data
plot(Pt, no_ris.sum_rate, 'LineWidth', 1.5, ...
    'Marker', 'v', 'MarkerIndices', 1:4:length(Pt));
hold on;
plot(Pt, ris32.sum_rate, 'LineWidth', 1.5, ...
    'Marker', 'x', 'MarkerIndices', 1:4:length(Pt));
plot(Pt, ris70.sum_rate, 'LineWidth', 1.5, ...
    'Marker', 's', 'MarkerIndices', 1:4:length(Pt));
plot(Pt, custom.sum_rate, 'LineWidth', 1.5, ...
    'Marker', '>', 'MarkerIndices', 1:4:length(Pt));

% Add labels and legend
xlabel('Transmit power per BS, $P_t$ (dBm)');
ylim([2 12.5])
xlim([-30 -10])
ylabel('Network sum-rate (bits/s/Hz)');
legend('Without RIS', '{$K$ = 34} Elements', '{$K$ = 70} Elements', ...
    '{$K$ = 70} Elements + Optimal PA', 'Location', 'northwest', 'FontSize', 10);

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% Contour Plot
load(".\results\results_exhaustive_es_aa.mat");
[X,Y] = meshgrid(bs2_assignment, beta_t);
smooth_factor = 9999; % You can adjust this parameter for desired smoothness
sum_rate_smooth = movmean(sum_rate, [52 30]);
[Xq, Yq] = meshgrid(linspace(double(min(X(:))), double(max(X(:))), 26), ...
    linspace(min(Y(:)), max(Y(:)), 1000));
sum_rate_interp = interp2(double(X), double(Y), sum_rate_smooth, Xq, Yq, "linear");
sum_rate_smooth = smoothdata(sum_rate_interp, 'loess', smooth_factor);
fig6 = figure(6);
[c, b] = contour(Xq, Yq, sum_rate_smooth, 10, 'LineWidth', 2);
shading interp;
% colormap jet
h = colorbar;
h.FontSize = 10;
h.TickLabelInterpreter = "latex";
h.Ticks = 8:0.1:8.5;
h.TickLabels = {"8", "8.1", "8.2", "8.3", "8.4", "8.5"};
% h.Label.String = "Network Sum-Rate (bits/s/Hz)";
clabel(c, b, 'manual', 'backgroundcolor', 'w');
xlabel('Element splitting ratio $\textbf{K}_A^1$ / $\textbf{K}_A^2$')
ylabel('Amplitude adjustments ratio $\beta_{t} / \beta_{r}$')
xtick = linspace(0, 70, 8);
ytick = linspace(0, 1, 11); % changed from 12 to 11
legend('Network sum-rate (bits/s/Hz)', 'Location', 'northwest', 'FontSize', 10)
set(gca, 'XTickLabel', {"0/70", "10/60", "20/50", "30/40", "40/30", ...
    "50/20", "60/10", "70/0"}, 'XTick', xtick);
set(gca,'YTickLabel',{"0/1", "0.1/0.9", "0.2/0.8", "0.3/0.7", ...
    "0.4/0.6", "0.5/0.5", "0.6/0.4", "0.7/0.3", "0.8/0.2", "0.9/0.1", "1/0"}, ...
    'YTick', ytick)

%% Export Graphics
exportgraphics(fig1, './resources/outage.pdf')
% exportgraphics(fig3, './resources/se_vs_ee.pdf')
% exportgraphics(fig4, './resources/rates.pdf')
% exportgraphics(fig5, './resources/sumrate.pdf')
% exportgraphics(fig6, './resources/dynamic.pdf')