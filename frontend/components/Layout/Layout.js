import Head from "next/head";
import Link from "next/link";
import SportsBasketballTwoToneIcon from "@mui/icons-material/SportsBasketballTwoTone";
import styles from "./Layout.module.css";

const Layout = ({ children, title = "r/nba Sentiments" }) => {
  return (
    <Link href="/" passHref>
      <div className={styles.container}>
        <Head>
          <title>{title}</title>
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <header className={styles.header}>
          <SportsBasketballTwoToneIcon fontSize="large" color="warning" />
          <h1>r/nba Sentiments 2021</h1>
        </header>
        <div className={styles.subtext}>
          <p>+/- Ratio = #Positive Mentions / #Negative Mentions</p>
          <p>Players with insufficient data not included</p>
        </div>
        <main className={styles.main}>{children}</main>
      </div>
    </Link>
  );
};

export default Layout;
