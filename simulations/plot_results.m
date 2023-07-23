% Define data
Pt = load("results\tx_power_-50.0dB_30.0dB").tx_power;

%% Links
link_both = load("results\res_32ris_enhanced_link_both.mat");
link_bs1 = load("results\res_32ris_enhanced_link_bs1_only.mat");
link_bs2 = load("results\res_32ris_enhanced_link_bs2_only.mat");
link_none = load("results\res_32ris_enhanced_link_none.mat");

fig1 = figure();
% Plot data
plot(Pt, link_both.sum_rate, 'LineWidth', 1.25, 'Marker', 'o', ...
    'MarkerIndices', 1:5:length(Pt));
hold on;
plot(Pt, link_bs1.sum_rate, 'LineWidth', 1.25, 'Marker', 's', ...
    'MarkerIndices', 1:5:length(Pt));
plot(Pt, link_bs2.sum_rate, 'LineWidth', 1.25, 'Marker', 'd', ...
    'MarkerIndices', 1:5:length(Pt));
plot(Pt, link_none.sum_rate, 'LineWidth', 1.25, 'Marker', 'p', ...
    'MarkerIndices', 1:5:length(Pt));

% Add labels and legend
xlabel('Transmit Power (dBm)');
ylim([0 18])
xlim([-30 0])
ylabel('Network Sum Rate (bits/s/Hz)');
legend('Both BS_{1} and BS_{2} Links', 'BS_{1} Link Only', ...
    'BS_{2} Link Only', 'No Direct Links', 'Location', 'southeast');

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% Outage
no_ris = load("results\res_no_ris.mat");
ris32 = load("results\res_32ris_enhanced_link_both.mat");
ris70 = load("results\res_70ris_enhanced_link_both.mat");

fig2 = figure();

semilogy(Pt, no_ris.outage(1, :), 'LineWidth', 1.25, ...
    'Marker', 'v', 'MarkerIndices', 1:5:length(Pt));
hold on;
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
xlabel('Transmit Power (dBm)');
ylim([5e-4 1])
xlim([-50 0])
ylabel('Outage Probability');
legend('No STAR-RIS, User U_{1c}', 'No STAR-RIS, User U_{2c}', ...
    'No STAR-RIS, User U_{f}', '{M = 32}, User U_{1c}', ...
    '{M = 32}, User U_{2c}', '{M = 32}, User U_{f}', ...
    '{M = 70}, User U_{1c}', '{M = 70}, User U_{2c}', ...
    '{M = 70}, User U_{f}', 'Location', 'southwest');

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% SE - EE
no_ris = load("results\res_no_ris.mat");
ris32 = load("results\res_32ris_enhanced_link_both.mat");
ris70 = load("results\res_70ris_enhanced_link_both.mat");

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
'Marker', 'o', 'MarkerIndices', i + 1);
    
% Add labels and legend
xlabel('Spectral Efficiency (bits/s/Hz)');
% ylim([5000 10000])
xlim([10 16])
ylabel('Energy Efficiency (bit/J)');
legend('No STAR-RIS', '{M = 32} Elements', '{M = 70} Elements', 'Location', 'southwest')

% Add grid
ax = gca;
ax.YAxis.Exponent=3;
grid('on');
set(gca, 'GridAlpha', 0.15);

%% User Rates
no_ris = load("results\res_no_ris.mat");
ris32 = load("results\res_32ris_enhanced_link_both.mat");
ris70 = load("results\res_70ris_enhanced_link_both.mat");

fig4 = figure();

% Plot data
plot(Pt, no_ris.rates(1, :), 'LineWidth', 1.25, ...
    'Marker', 'v', 'MarkerIndices', 1:5:length(Pt));
hold on;
plot(Pt, no_ris.rates(2, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, no_ris.rates(3, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:5:length(Pt));

plot(Pt, ris32.rates(1, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, ris32.rates(2, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, ris32.rates(3, :), 'LineWidth', 1.25, ...
'Marker', 'o', 'MarkerIndices', 1:5:length(Pt));

plot(Pt, ris70.rates(1, :), 'LineWidth', 1.25, ...
    'Marker', 'x', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, ris70.rates(2, :), 'LineWidth', 1.25, ...
    'Marker', 's', 'MarkerIndices', 1:5:length(Pt));
plot(Pt, ris70.rates(3, :), 'LineWidth', 1.25, ...
    'Marker', 'd', 'MarkerIndices', 1:5:length(Pt));
    
% Add labels and legend
xlabel('Transmit Power (dBm)');
ylim([0 10])
xlim([-50 10])
ylabel('Rates (bits/s/Hz)');
legend('No STAR-RIS, User U_{1c}', 'No STAR-RIS, User U_{2c}', ...
    'No STAR-RIS, User U_{f}', '{M = 32}, User U_{1c}', ...
    '{M = 32}, User U_{2c}', '{M = 32}, User U_{f}', ...
    '{M = 70}, User U_{1c}', '{M = 70}, User U_{2c}', ...
    '{M = 70}, User U_{f}', 'Location', 'northwest');

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% Sum Rate
no_ris = load("results\res_no_ris.mat");
ris32 = load("results\res_32ris_enhanced_link_both.mat");
ris70 = load("results\res_70ris_enhanced_link_both.mat");
custom = load("results\res_70ris_enhanced_link_both_custom.mat");

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
xlabel('Transmit Power (dBm)');
% ylim([0 20])
xlim([-30 -10])
ylabel('Network Sum Rate (bits/s/Hz)');
legend('No STAR-RIS', '{M = 32} Elements', '{M = 70} Elements', ...
    '{M = 70} Elements + Optimized PA', 'Location', 'northwest');

% Add grid
grid('on');
set(gca, 'GridAlpha', 0.15);

%% Export Graphics
exportgraphics(fig1, '../resources/figs/links.pdf')
exportgraphics(fig2, '../resources/figs/outage.pdf')
exportgraphics(fig3, '../resources/figs/se_vs_ee.pdf')
exportgraphics(fig4, '../resources/figs/rates.pdf')
exportgraphics(fig5, '../resources/figs/sumrate.pdf')