% Define data
clear;
close all;
Pt = load("results\tx_power_dB.mat").tx_power;

%% Links
% link_both = load("results\res_32ris_enhanced_link_both.mat");
% link_bs1 = load("results\res_32ris_enhanced_link_bs1_only.mat");
% link_bs2 = load("results\res_32ris_enhanced_link_bs2_only.mat");
% link_none = load("results\res_32ris_enhanced_link_none.mat");
% 
% fig1 = figure();
% % Plot data
% plot(Pt, link_both.sum_rate, 'LineWidth', 1.25, 'Marker', 'o', ...
%     'MarkerIndices', 1:5:length(Pt));
% hold on;
% plot(Pt, link_bs1.sum_rate, 'LineWidth', 1.25, 'Marker', 's', ...
%     'MarkerIndices', 1:5:length(Pt));
% plot(Pt, link_bs2.sum_rate, 'LineWidth', 1.25, 'Marker', 'd', ...
%     'MarkerIndices', 1:5:length(Pt));
% plot(Pt, link_none.sum_rate, 'LineWidth', 1.25, 'Marker', 'p', ...
%     'MarkerIndices', 1:5:length(Pt));
% 
% % Add labels and legend
% xlabel('Transmit Power per BS (dBm)');
% ylim([0 18])
% xlim([-30 0])
% ylabel('Network Sum Rate (bits/s/Hz)');
% legend('Both BS_{1} and BS_{2} Links', 'BS_{1} Link Only', ...
%     'BS_{2} Link Only', 'No Direct Links', 'Location', 'southeast');
% 
% % Add grid
% grid('on');
% set(gca, 'GridAlpha', 0.15);

%% Outage
no_ris_non_comp = load("results\results_no_ris_non_comp.mat");
no_ris = load("results\results_no_ris.mat");
ris32 = load("results\results_ris32.mat");
ris70 = load("results\results_ris70.mat");

fig2 = figure();

semilogy(Pt, no_ris_non_comp.outage(3, :), 'LineWidth', 1.25, ...
    'Marker', '>', 'MarkerIndices', 1:5:length(Pt));
hold on;
semilogy(Pt, no_ris.outage(1, :), 'LineWidth', 1.25, ...
    'Marker', 'v', 'MarkerIndices', 1:5:length(Pt));
semilogy(Pt, no_ris.outage(2, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:5:length(Pt));
semilogy(Pt, no_ris.outage(3, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:5:length(Pt));

semilogy(Pt, ris32.outage(1, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:5:length(Pt));
semilogy(Pt, ris32.outage(2, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:5:length(Pt));
semilogy(Pt, ris32.outage(3, :), 'LineWidth', 1.25, ...
'Marker', 'o', 'MarkerIndices', 1:5:length(Pt));

semilogy(Pt, ris70.outage(1, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:5:length(Pt));
semilogy(Pt, ris70.outage(2, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:5:length(Pt));
semilogy(Pt, ris70.outage(3, :), 'LineWidth', 1.25, ...
    'Marker', 'd', 'MarkerIndices', 1:5:length(Pt));
    
% Add labels and legend
xlabel('Transmit Power per BS (dBm)');
ylim([9e-4 1])
xlim([-45 0])
ylabel('Outage Probability');
legend('User U_{f}, Non-CoMP, without RIS', ...
    'User U_{1,m}, without RIS', 'User U_{2,n}, without RIS', ...
    'User U_{f}, without RIS', 'User U_{1,m}, {K = 32} Elements', ...
    'User U_{2,n}, {K = 32} Elements', 'User U_{f}, {K = 32} Elements', ...
    'User U_{1,m}, {K = 70} Elements', 'User U_{2,n}, {K = 70} Elements', ...
    'User U_{f}, {K = 70} Elements', 'Location', 'southwest');

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% SE - EE
no_ris = load("results\results_no_ris.mat");
ris32 = load("results\results_ris32.mat");
ris70 = load("results\results_ris70.mat");

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
xlabel('Spectral Efficiency (bits/s/Hz)');
% ylim([5000 10000])
xlim([10 16])
ylabel('Energy Efficiency (bit/J)');
legend('Without RIS', '{K = 32} Elements', '{K = 70} Elements', 'Location', 'southwest')

% Add grid
ax = gca;
ax.YAxis.Exponent=3;
grid('on');
set(gca, 'GridAlpha', 0.15);

%% User Rates
no_ris_non_comp = load("results\results_no_ris_non_comp.mat");
no_ris = load("results\results_no_ris.mat");
ris32 = load("results\results_ris32.mat");
ris70 = load("results\results_ris70.mat");

fig4 = figure();

% Plot data
plot(Pt, no_ris_non_comp.rates(3, :), 'LineWidth', 1.25, ...
    'Marker', '+', 'MarkerIndices', 1:5:length(Pt));
hold on;
plot(Pt, no_ris.rates(1, :), 'LineWidth', 1.25, ...
    'Marker', 'v', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, no_ris.rates(2, :), 'LineWidth', 1.25, ...
    'Marker', '<', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, no_ris.rates(3, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:5:length(Pt));

plot(Pt, ris32.rates(1, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, ris32.rates(2, :), 'LineWidth', 1.25, ...
    'Marker', '>', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, ris32.rates(3, :), 'LineWidth', 1.25, ...
'Marker', 'o', 'MarkerIndices', 1:5:length(Pt));

plot(Pt, ris70.rates(1, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, ris70.rates(2, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, ris70.rates(3, :), 'LineWidth', 1.25, ...
    'Marker', 'd', 'MarkerIndices', 1:5:length(Pt));

% Add labels and legend
xlabel('Transmit Power per BS (dBm)');
ylim([0 7])
xlim([-45 0])
ylabel('Rates (bits/s/Hz)');
legend('User U_{f}, Non-CoMP, without RIS', ...
    'User U_{1,m}, without RIS', 'User U_{2,n}, without RIS', ...
    'User U_{f}, without RIS', 'User U_{1,m}, {K = 32} Elements', ...
    'User U_{2,n}, {K = 32} Elements', 'User U_{f}, {K = 32} Elements', ...
    'User U_{1,m}, {K = 70} Elements', 'User U_{2,n}, {K = 70} Elements', ...
    'User U_{f}, {K = 70} Elements', 'Location', 'northwest');

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% Sum Rate
no_ris = load("results\results_no_ris.mat");
ris32 = load("results\results_ris32.mat");
ris70 = load("results\results_ris70.mat");
custom = load("results\results_ris70_oPA.mat");

fig5 = figure();

% Plot data
plot(Pt, no_ris.sum_rate, 'LineWidth', 1.25, ...
    'Marker', 'v', 'MarkerIndices', 1:2:length(Pt));
hold on;
plot(Pt, ris32.sum_rate, 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:2:length(Pt));
plot(Pt, ris70.sum_rate, 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:2:length(Pt));
plot(Pt, custom.sum_rate, 'LineWidth', 1.25, ...
    'Marker', '>', 'MarkerIndices', 1:2:length(Pt));

% Add labels and legend
xlabel('Transmit Power per BS (dBm)');
ylim([0 12.5])
xlim([-35 -10])
ylabel('Network Sum Rate (bits/s/Hz)');
legend('Without RIS', '{K = 32} Elements', '{K = 70} Elements', ...
    '{K = 70} Elements + Optimal PA', 'Location', 'northwest');

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% Contour Plot
load("results\results_exhaustive_es_aa.mat");
[X,Y] = meshgrid(bs2_assignment, beta_t);
sum_rate_smooth = movmean(sum_rate, [20 20]);
[Xq, Yq] = meshgrid(linspace(double(min(X(:))), double(max(X(:))), 15), ...
    linspace(min(Y(:)), max(Y(:)), 15));
sum_rate_interp = interp2(double(X), double(Y), sum_rate_smooth, Xq, Yq, "linear");

fig6 = figure(6);
contourf(Xq, Yq, sum_rate_interp, 250, 'EdgeColor', 'flat')
shading interp;
% colormap jet
h = colorbar;
h.Label.String = "Network Sum-Rate (bits/s/Hz)";
h.Label.FontSize = 11;
xlabel('Element Splitting Ratio BS_{1} / BS_{2}', ...
    'Interpreter', 'tex')
ylabel('Amplitude Coefficients Ratio \beta_{t} / \beta_{r}', ...
    'Interpreter', 'tex')
xtick = linspace(0, 70, 8);
ytick = linspace(0, 1, 11); % changed from 12 to 11
set(gca, 'XTickLabel', {"0/70", "10/60", "20/50", "30/40", "40/30", ...
    "50/20", "60/10", "70/0"}, 'XTick', xtick);
set(gca,'YTickLabel',{"0/1", "0.1/0.9", "0.2/0.8", "0.3/0.7", ...
    "0.4/0.6", "0.5/0.5", "0.6/0.4", "0.7/0.3", "0.8/0.2", "0.9/0.1", "1/0"}, ...
    'YTick', ytick)

%% Export Graphics
% exportgraphics(fig1, '../resources/links.pdf')
exportgraphics(fig2, '../resources/outage.pdf')
exportgraphics(fig3, '../resources/se_vs_ee.pdf')
exportgraphics(fig4, '../resources/rates.pdf')
exportgraphics(fig5, '../resources/sumrate.pdf')
exportgraphics(fig6, '../resources/dynamic.pdf')