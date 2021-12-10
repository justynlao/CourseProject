import Link from "next/link";
import Image from "next/image";
import SentimentVerySatisfiedIcon from "@mui/icons-material/SentimentVerySatisfied";
import SentimentNeutralIcon from "@mui/icons-material/SentimentNeutral";
import SentimentVeryDissatisfiedIcon from "@mui/icons-material/SentimentVeryDissatisfied";
import styles from "./PlayerList.module.css";

const PlayerList = ({ players }) => {
  const filtered_players = players.filter((player) => {
    const { title_polarity_counts, comment_polarity_counts } = player;
    const total_pos = +title_polarity_counts.positive + +comment_polarity_counts.positive;
    const total_neg = +title_polarity_counts.negative + +comment_polarity_counts.negative;
    const positivity_index = (total_pos / total_neg).toFixed(2);
    return !isNaN(positivity_index);
  });
  return (
    <div className={styles.list_container}>
      {filtered_players.map((player, index) => {
        const { player_id, full_name, title_polarity_counts, comment_polarity_counts } = player;
        const total_pos = +title_polarity_counts.positive + +comment_polarity_counts.positive;
        const total_neg = +title_polarity_counts.negative + +comment_polarity_counts.negative;
        const positivity_index = (total_pos / total_neg).toFixed(2);
        const avatar_url = `https://cdn.nba.com/headshots/nba/latest/260x190/${player_id}.png`;
        return (
          <Link href="/player/[id]" as={`/player/${player_id}`} key={index} passHref>
            <div className={styles.list_item}>
              <div className={styles.avatar}>
                <Image src={avatar_url} alt={full_name} width="130px" height="95px" />
              </div>
              <div className={styles.list_text}>
                <h2>{full_name}</h2>
                <h3>+/- Ratio: {positivity_index}</h3>
                {positivity_index >= 3 ? (
                  <SentimentVerySatisfiedIcon color="success" fontSize="large" />
                ) : positivity_index >= 2 ? (
                  <SentimentNeutralIcon color="warning" fontSize="large" />
                ) : (
                  <SentimentVeryDissatisfiedIcon color="error" fontSize="large" />
                )}
              </div>
            </div>
          </Link>
        );
      })}
    </div>
  );
};

export default PlayerList;
