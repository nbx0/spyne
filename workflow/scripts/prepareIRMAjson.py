import pandas as pd
import json
from sys import argv, path, exit, executable
import os.path as op
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

path.append(op.dirname(op.realpath(__file__)))
import irma2pandas  # type: ignore
import dais2pandas  # type: ignore

try:
    irma_path = argv[1]
except IndexError:
    exit(
        f"\n\tUSAGE: python {__file__} <path/to/irma/results/>\n"
        f"\n\t\t*Inside path/to/irma/results should be the individual samples-irma-dir results\n"
        f"\n\tYou entered:\n\t{executable} {' '.join(argv)}\n\n"
    )


def pivot4heatmap(coverage_df):
    if "Coverage_Depth" in coverage_df.columns:
        cov_header = "Coverage_Depth"
    else:
        cov_header = "Coverage Depth"
    df2 = coverage_df[["Sample", "Reference_Name", cov_header]]
    df3 = df2.groupby(["Sample", "Reference_Name"]).mean().reset_index()
    try:
        df3[["Subtype", "Segment", "Group"]] = df3["Reference_Name"].str.split(
            "_", expand=True
        )
    except ValueError:
        df3["Segment"] = df3["Reference_Name"]
    df4 = df3[["Sample", "Segment", cov_header]]
    return df4


def createheatmap(irma_path, coverage_means_df):
    print(f"Building coverage heatmap")
    if "Coverage_Depth" in coverage_means_df.columns:
        cov_header = "Coverage_Depth"
    else:
        cov_header = "Coverage Depth"
    cov_max = coverage_means_df[cov_header].max()
    if cov_max <= 200:
        cov_max = 200
    fig = go.Figure(
        data=go.Heatmap(  # px.imshow(df5
            x=list(coverage_means_df["Sample"]),
            y=list(coverage_means_df["Segment"]),
            z=list(coverage_means_df[cov_header]),
            zmin=0,
            zmid=100,
            zmax=cov_max,
            colorscale="Blugrn",
            hovertemplate="%{y} = %{z:,.0f}x<extra>%{x}<br></extra>",
        )
    )
    fig.update_layout(legend=dict(x=0.4, y=1.2, orientation="h"))
    fig.update_xaxes(side="top")
    pio.write_json(fig, f"{irma_path}/heatmap.json")
    print(f"  -> coverage heatmap json saved to {irma_path}/heatmap.json")


def createsankey(irma_path, read_df):
    print(f"Building read sankey plot")
    for sample in read_df["Sample"].unique():
        sankeyfig = irma2pandas.dash_reads_to_sankey(
            read_df[read_df["Sample"] == sample]
        )
        pio.write_json(sankeyfig, f"{irma_path}/readsfig_{sample}.json")
        print(f"  -> read sankey plot json saved to {irma_path}/readsfig_{sample}.json")


def createSampleCoverageFig(sample, df, segments, segcolor, cov_linear_y):
    if "Coverage_Depth" in df.columns:
        cov_header = "Coverage_Depth"
    else:
        cov_header = "Coverage Depth"
    if "HMM_Position" in df.columns:
        pos_header = "HMM_Position"
    else:
        pos_header = "Position"

    def zerolift(x):
        if x == 0:
            return 0.000000000001
        return x

    if not cov_linear_y:
        df[cov_header] = df[cov_header].apply(lambda x: zerolift(x))
    df2 = df[df["Sample"] == sample]
    fig = go.Figure()
    if "SARS-CoV-2" in segments:
        # y positions for gene boxes
        oy = (
            max(df2[cov_header]) / 10
        )  # This value determines where the top of the ORF box is drawn against the y-axis
        if not cov_linear_y:
            ya = 0.9
        else:
            ya = 0 - (max(df2[cov_header]) / 20)
        orf_pos = {
            "orf1ab": (266, 21556),
            "S": [21563, 25385],
            "orf3a": [25393, 26221],
            "E": [26245, 26473],
            "M": [26523, 27192],
            "orf6": [27202, 27388],
            "orf7ab": [27394, 27888],
            "orf8": [27894, 28260],
            "N": [28274, 29534],
            "orf10": [29558, 29675],
        }
        color_index = 0
        for orf, pos in orf_pos.items():
            fig.add_trace(
                go.Scatter(
                    x=[pos[0], pos[1], pos[1], pos[0], pos[0]],
                    y=[oy, oy, 0, 0, oy],
                    fill="toself",
                    fillcolor=px.colors.qualitative.T10[color_index],
                    line=dict(color=px.colors.qualitative.T10[color_index]),
                    mode="lines",
                    name=orf,
                    opacity=0.4,
                )
            )
            color_index += 1
    for g in segments:
        if g in df2["Reference_Name"].unique():
            try:
                g_base = g.split("_")[1]
            except IndexError:
                g_base = g
            df3 = df2[df2["Reference_Name"] == g]
            fig.add_trace(
                go.Scatter(
                    x=df3[pos_header],
                    y=df3[cov_header],
                    mode="lines",
                    line=go.scatter.Line(color=segcolor[g_base]),
                    name=g,
                    customdata=tuple(["all"] * len(df3["Sample"])),
                )
            )
    fig.add_shape(
        type="line",
        x0=0,
        x1=df2[pos_header].max(),
        y0=100,
        y1=100,
        line=dict(color="Black", dash="dash", width=5),
    )
    ymax = df2[cov_header].max()
    if not cov_linear_y:
        ya_type = "log"
        ymax = ymax ** (1 / 10)
    else:
        ya_type = "linear"
    fig.update_layout(
        height=600,
        title=sample,
        yaxis_title="Coverage",
        xaxis_title="Reference Position",
        yaxis_type=ya_type,
        yaxis_range=[0, ymax],
    )
    return fig


def createcoverageplot(irma_path, coverage_df, segments, segcolor):
    samples = coverage_df["Sample"].unique()
    print(f"Building coverage plots for {len(samples)} samples")
    for sample in samples:
        coveragefig = createSampleCoverageFig(
            sample, coverage_df, segments, segcolor, False
        )
        pio.write_json(coveragefig, f"{irma_path}/coveragefig_{sample}_linear.json")
        print(f"  -> saved {irma_path}/coveragefig_{sample}_linear.json")
        coveragefig = createSampleCoverageFig(
            sample, coverage_df, segments, segcolor, True
        )
        pio.write_json(coveragefig, f"{irma_path}/coveragefig_{sample}_log.json")
        print(f"  -> saved {irma_path}/coveragefig_{sample}_log.json")
    print(f" --> All coverage jsons saved")


def generate_figs(irma_path, read_df, coverage_df, segments, segcolor):
    createsankey(irma_path, read_df)
    createheatmap(irma_path, pivot4heatmap(coverage_df))
    createcoverageplot(irma_path, coverage_df, segments, segcolor)


def generate_dfs(irma_path):
    print("Building coverage_df")
    coverage_df = irma2pandas.dash_irma_coverage_df(irma_path)
    with open(f"{irma_path}/coverage.json", "w") as out:
        coverage_df.to_json(out, orient="split", double_precision=3)
        print(f"  -> coverage_df saved to {out.name}")
    print("Building read_df")
    read_df = irma2pandas.dash_irma_reads_df(irma_path)
    with open(f"{irma_path}/reads.json", "w") as out:
        read_df.to_json(out, orient="split", double_precision=3)
        print(f"  -> read_df saved to {out.name}")
    print("Building alleles_df")
    alleles_df = irma2pandas.dash_irma_alleles_df(irma_path)
    with open(f"{irma_path}/alleles.json", "w") as out:
        alleles_df.to_json(out, orient="split", double_precision=3)
        print(f"  -> alleles_df saved to {out.name}")
    print("Building indels_df")
    indels_df = irma2pandas.dash_irma_indels_df(irma_path)
    with open(f"{irma_path}/indels.json", "w") as out:
        indels_df.to_json(out, orient="split", double_precision=3)
        print(f"  -> indels_df saved to {out.name}")
    print("Building ref_data")
    ref_lens = irma2pandas.reference_lens(irma_path)
    segments, segset, segcolor = irma2pandas.returnSegData(coverage_df)
    with open(f"{irma_path}/ref_data.json", "w") as out:
        json.dump(
            {
                "ref_lens": ref_lens,
                "segments": segments,
                "segset": segset,
                "segcolor": segcolor,
            },
            out,
        )
        print(f"  -> ref_data saved to {out.name}")
    print("Building dais_vars_df")
    dais_vars_df = dais2pandas.compute_dais_variants(f"{irma_path}/dais_results")
    with open(f"{irma_path}/dais_vars.json", "w") as out:
        dais_vars_df.to_json(out, orient="split", double_precision=3)
        print(f"  -> dais_vars_df saved to {out.name}")
    return read_df, coverage_df, segments, segcolor


if __name__ == "__main__":
    generate_figs(irma_path, *generate_dfs(irma_path))
