import { useState } from "react";
import PlayerList from "../components/PlayerList/PlayerList";
import SearchBar from "../components/SearchBar/SearchBar";
import axios from "axios";
import { MongoClient } from "mongodb";
import styles from "../styles/Home.module.css";

export default function Home({ data }) {
  const [searchField, setSearchField] = useState("");

  const filteredPlayers = data.filter((player) => {
    return player.full_name.toLowerCase().includes(searchField);
  });

  const onSearchChange = (event) => {
    event.preventDefault();
    setSearchField(event.target.value.toLowerCase());
  };

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <SearchBar handleSearchChange={onSearchChange} />
        <PlayerList players={filteredPlayers} />
      </main>
    </div>
  );
}

export const getStaticProps = async () => {
  const client = await MongoClient.connect(`mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@cluster0.yfg5a.mongodb.net/playerSentiments?retryWrites=true&w=majority`)
  const db = client.db();
  const players = db.collection("players");
  const data = await players.find({}, {projection: {_id: 0}}).toArray();
  client.close();

  return {
    props: {
      data,
    },
  };
};
