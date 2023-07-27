% Define data
clear;
close all;
set(groot,'defaulttextinterpreter','latex');
set(groot, 'defaultLegendInterpreter','latex');
set(groot, 'defaultAxesTickLabelInterpreter','latex');
Pt = load("..\resources\data\tx_power_dB.mat").tx_power;

%% Links
% link_both = load("..\resources\data\res_32ris_enhanced_link_both.mat");
% link_bs1 = load("..\resources\data\res_32ris_enhanced_link_bs1_only.mat");
% link_bs2 = load("..\resources\data\res_32ris_enhanced_link_bs2_only.mat");
% link_none = load("..\resources\data\res_32ris_enhanced_link_none.mat");
% 
% fig1 = figure();
% % Plot data
% plot(Pt, link_both.sum_rate, 'LineWidth', 1.25, 'Marker', 'o', ...
%     'MarkerIndices', 1:10:length(Pt));
% hold on;
% plot(Pt, link_bs1.sum_rate, 'LineWidth', 1.25, 'Marker', 's', ...
%     'MarkerIndices', 1:10:length(Pt));
% plot(Pt, link_bs2.sum_rate, 'LineWidth', 1.25, 'Marker', 'd', ...
%     'MarkerIndices', 1:10:length(Pt));
% plot(Pt, link_none.sum_rate, 'LineWidth', 1.25, 'Marker', 'p', ...
%     'MarkerIndices', 1:10:length(Pt));
% 
% % Add labels and legend
% xlabel('Transmit power per BS, $P_t$ (dBm)');
% ylim([0 18])
% xlim([-30 0])
% ylabel('Network sum-rate (bits/s/Hz)');
% legend('Both BS_{1} and BS_{2} Links', 'BS_{1} Link Only', ...
%     'BS_{2} Link Only', 'No Direct Links', 'Location', 'southeast');
% 
% % Add grid
% grid('on');
% set(gca, 'GridAlpha', 0.15);

%% Outage
no_ris_non_comp = load("..\resources\data\results_no_ris_non_comp.mat");
no_ris = load("..\resources\data\results_no_ris.mat");
ris32 = load("..\resources\data\results_ris32.mat");
ris70 = load("..\resources\data\results_ris70.mat");

fig2 = figure();

semilogy(Pt, no_ris_non_comp.outage(3, :), 'LineWidth', 1.25, ...
    'Marker', '>', 'MarkerIndices', 1:10:length(Pt));
hold on;
semilogy(Pt, no_ris.outage(1, :), 'LineWidth', 1.25, ...
    'Marker', 'v', 'MarkerIndices', 1:10:length(Pt));
semilogy(Pt, no_ris.outage(2, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:10:length(Pt));
semilogy(Pt, no_ris.outage(3, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:10:length(Pt));

semilogy(Pt, ris32.outage(1, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:10:length(Pt));
semilogy(Pt, ris32.outage(2, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:10:length(Pt));
semilogy(Pt, ris32.outage(3, :), 'LineWidth', 1.25, ...
'Marker', 'o', 'MarkerIndices', 1:10:length(Pt));

semilogy(Pt, ris70.outage(1, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:10:length(Pt));
semilogy(Pt, ris70.outage(2, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:10:length(Pt));
semilogy(Pt, ris70.outage(3, :), 'LineWidth', 1.25, ...
    'Marker', 'd', 'MarkerIndices', 1:10:length(Pt));
    
% Add labels and legend
xlabel('Transmit power per BS, $P_t$ (dBm)');
ylim([9e-4 1])
xlim([-45 0])
ylabel('Outage probability');
legend('U$_{f}$, Non-CoMP, without RIS', ...
    'U$_{1,c}$, without RIS', 'U$_{2,c}$, without RIS', ...
    'U$_{f}$, without RIS', 'U$_{1,c}$, {K = 32} Elements', ...
    'U$_{2,c}$, {K = 32} Elements', 'U$_{f}$, {K = 32} Elements', ...
    'U$_{1,c}$, {K = 70} Elements', 'U$_{2,c}$, {K = 70} Elements', ...
    'U$_{f}$, {K = 70} Elements', 'Location', 'southwest', 'FontSize', 10);

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% SE - EE
no_ris = load("..\resources\data\results_no_ris.mat");
ris32 = load("..\resources\data\results_ris32.mat");
ris70 = load("..\resources\data\results_ris70.mat");

fig3 = figure();

% Plot data
[~, i] = max(no_ris.ee);
plot(no_ris.se, no_ris.ee, 'LineWidth', 1.25, ...
    'Marker', 'v', 'MarkerIndices', i);
hold on;
[~, i] = max(ris32.ee);
plot(ris32.se, ris32.ee, 'LineWidth', 1.25, ...
    'Marker', 'd', 'MarkerIndices', i);
[~, i] = max(ris70.ee);
plot(ris70.se, ris70.ee, 'LineWidth', 1.25, ...
'Marker', 'o', 'MarkerIndices', i);
    
% Add labels and legend
xlabel('Spectral efficiency (bits/s/Hz)');
ylim([9000 11000])
xlim([11 17])
ylabel('Energy efficiency (bit/J)');
legend('Without RIS', '{K = 32} Elements', '{K = 70} Elements', ...
    'Location', 'southwest', 'FontSize', 10)

% Add grid
ax = gca;
ax.YAxis.Exponent=3;
grid('on');
set(gca, 'GridAlpha', 0.15);

%% User Rates
no_ris_non_comp = load("..\resources\data\results_no_ris_non_comp.mat");
no_ris = load("..\resources\data\results_no_ris.mat");
ris32 = load("..\resources\data\results_ris32.mat");
ris70 = load("..\resources\data\results_ris70.mat");

fig4 = figure();

% Plot data
plot(Pt, no_ris_non_comp.rates(3, :), 'LineWidth', 1.25, ...
    'Marker', '+', 'MarkerIndices', 1:10:length(Pt));
hold on;
plot(Pt, no_ris.rates(1, :), 'LineWidth', 1.25, ...
    'Marker', 'v', 'MarkerIndices', 1:10:length(Pt));
plot(Pt, no_ris.rates(2, :), 'LineWidth', 1.25, ...
    'Marker', '<', 'MarkerIndices', 1:10:length(Pt));
plot(Pt, no_ris.rates(3, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:10:length(Pt));

plot(Pt, ris32.rates(1, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:10:length(Pt));
plot(Pt, ris32.rates(2, :), 'LineWidth', 1.25, ...
    'Marker', '>', 'MarkerIndices', 1:10:length(Pt));
plot(Pt, ris32.rates(3, :), 'LineWidth', 1.25, ...
'Marker', 'o', 'MarkerIndices', 1:10:length(Pt));

plot(Pt, ris70.rates(1, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:10:length(Pt));
plot(Pt, ris70.rates(2, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:10:length(Pt));
plot(Pt, ris70.rates(3, :), 'LineWidth', 1.25, ...
    'Marker', 'd', 'MarkerIndices', 1:10:length(Pt));

% Add labels and legend
xlabel('Transmit power per BS, $P_t$ (dBm)');
ylim([0 7])
xlim([-45 0])
ylabel('User rates (bits/s/Hz)');
legend('U$_{f}$, Non-CoMP, without RIS', ...
    'U$_{1,c}$, without RIS', 'U$_{2,c}$, without RIS', ...
    'U$_{f}$, without RIS', 'U$_{1,c}$, {K = 32} Elements', ...
    'U$_{2,c}$, {K = 32} Elements', 'U$_{f}$, {K = 32} Elements', ...
    'U$_{1,c}$, {K = 70} Elements', 'U$_{2,c}$, {K = 70} Elements', ...
    'U$_{f}$, {K = 70} Elements', 'Location', 'northwest', 'FontSize', 10);

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% Sum-rate
no_ris = load("..\resources\data\results_no_ris.mat");
ris32 = load("..\resources\data\results_ris32.mat");
ris70 = load("..\resources\data\results_ris70.mat");
custom = load("..\resources\data\results_ris70_oPA.mat");

fig5 = figure();

% Plot data
plot(Pt, no_ris.sum_rate, 'LineWidth', 1.25, ...
    'Marker', 'v', 'MarkerIndices', 1:4:length(Pt));
hold on;
plot(Pt, ris32.sum_rate, 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:4:length(Pt));
plot(Pt, ris70.sum_rate, 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:4:length(Pt));
plot(Pt, custom.sum_rate, 'LineWidth', 1.25, ...
    'Marker', '>', 'MarkerIndices', 1:4:length(Pt));

% Add labels and legend
xlabel('Transmit power per BS, $P_t$ (dBm)');
ylim([2 12.5])
xlim([-30 -10])
ylabel('Network sum-rate (bits/s/Hz)');
legend('Without RIS', '{K = 32} Elements', '{K = 70} Elements', ...
    '{K = 70} Elements + Optimal PA', 'Location', 'northwest', 'FontSize', 10);

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% Contour Plot
load("..\resources\data\results_exhaustive_es_aa.mat");
[X,Y] = meshgrid(bs2_assignment, beta_t);
smooth_factor = 9999; % You can adjust this parameter for desired smoothness
sum_rate_smooth = movmean(sum_rate, [52 30]);
[Xq, Yq] = meshgrid(linspace(double(min(X(:))), double(max(X(:))), 26), ...
    linspace(min(Y(:)), max(Y(:)), 1000));
sum_rate_interp = interp2(double(X), double(Y), sum_rate_smooth, Xq, Yq, "linear");
sum_rate_smooth = smoothdata(sum_rate_interp, 'loess', smooth_factor);
fig6 = figure(6);
[c, b] = contour(Xq, Yq, sum_rate_smooth, 10, 'LineWidth', 1.5);
shading interp;
% colormap jet
h = colorbar;
h.FontSize = 10;
h.TickLabelInterpreter = "latex";
h.Ticks = 8:0.1:8.5;
h.TickLabels = {"8", "8.1", "8.2", "8.3", "8.4", "8.5"};
% h.Label.String = "Network Sum-Rate (bits/s/Hz)";
clabel(c, b, 'manual', 'backgroundcolor', 'w');
xlabel('Element splitting ratio $\mathrm{BS}_{1}$ / $\mathrm{BS}_{2}$')
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
% exportgraphics(fig1, '../resources/links.pdf')
% exportgraphics(fig2, '../resources/outage.pdf')
% exportgraphics(fig3, '../resources/se_vs_ee.pdf')
% exportgraphics(fig4, '../resources/rates.pdf')
% exportgraphics(fig5, '../resources/sumrate.pdf')
% exportgraphics(fig6, '../resources/dynamic.pdf')