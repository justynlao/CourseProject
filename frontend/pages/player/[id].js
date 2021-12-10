import PlayerDetails from "../../components/PlayerDetails/PlayerDetails";
import axios from "axios";
import { MongoClient } from "mongodb";
import _fetch from "isomorphic-fetch";
import styles from "../../styles/Player.module.css";

export default function Player({ data }) {
  return (
    <main className={styles.main}>
      <PlayerDetails player={data}></PlayerDetails>
    </main>
  );
}

export const getStaticProps = async (context) => {
  const id = context?.params?.id;
  const client = await MongoClient.connect(`mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@cluster0.yfg5a.mongodb.net/playerSentiments?retryWrites=true&w=majority`)
  const db = client.db();
  const players = db.collection("players");
  const data = await players.findOne({player_id: +id}, {projection: {_id: 0}});
  client.close();

  return {
    props: {
      data,
    },
  };
};

export const getStaticPaths = async () => {
  const client = await MongoClient.connect(`mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@cluster0.yfg5a.mongodb.net/playerSentiments?retryWrites=true&w=majority`)
  const db = client.db();
  const players = db.collection("players");
  const data = await players.find({}, {projection: {_id: 0}}).toArray();
  client.close();

  const paths = data.map((player) => {
    return {
      params: { id: player.player_id.toString() },
    };
  });

  return {
    paths,
    fallback: false,
  };
};
