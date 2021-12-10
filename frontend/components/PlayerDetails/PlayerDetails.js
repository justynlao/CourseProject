import Image from "next/image";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Doughnut } from "react-chartjs-2";
import SentimentVerySatisfiedIcon from "@mui/icons-material/SentimentVerySatisfied";
import SentimentNeutralIcon from "@mui/icons-material/SentimentNeutral";
import SentimentVeryDissatisfiedIcon from "@mui/icons-material/SentimentVeryDissatisfied";

import styles from "./PlayerDetails.module.css";

ChartJS.register(ArcElement, Tooltip, Legend);

const PlayerDetails = ({ player }) => {
  const { player_id, full_name, title_polarity_counts, comment_polarity_counts } = player;
  const total_pos = +title_polarity_counts.positive + +comment_polarity_counts.positive;
  const total_neg = +title_polarity_counts.negative + +comment_polarity_counts.negative;
  const total_neu = +title_polarity_counts.neutral + +comment_polarity_counts.neutral;
  const positivity_index = (total_pos / total_neg).toFixed(2);

  const img_url = `https://cdn.nba.com/headshots/nba/latest/1040x760/${player_id}.png`;
  const labels = ["Positive", "Neutral", "Negative"];
  const label_data = [total_pos, total_neu, total_neg];

  const chart_data = {
    labels: labels,
    datasets: [
      {
        data: label_data,
        backgroundColor: [
          "rgba(75, 192, 192, 0.2)",
          "rgba(255, 165, 0, 0.2)",
          "rgba(255, 99, 132, 0.2)",
        ],
        borderColor: ["rgba(75, 192, 192, 1)", "rgba(255, 165, 0, 1)", "rgba(255, 99, 132, 1)"],
        borderWidth: 1,
        hoverOffset: 4,
      },
    ],
  };

  return (
    <div className={styles.details}>
      <header className={styles.detail_header}>
        <h2>{full_name}</h2>
        <Image src={img_url} alt={full_name} width="256px" height="190px" />
        <h3>+/- Ratio: {positivity_index}</h3>
        {positivity_index >= 3 ? (
          <SentimentVerySatisfiedIcon color="success" fontSize="large" />
        ) : positivity_index >= 2 ? (
          <SentimentNeutralIcon color="warning" fontSize="large" />
        ) : (
          <SentimentVeryDissatisfiedIcon color="error" fontSize="large" />
        )}
      </header>
      <Doughnut data={chart_data}/>
    </div>
  );
};

export default PlayerDetails;
