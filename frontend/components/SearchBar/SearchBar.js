import SearchIcon from "@mui/icons-material/Search";
import styles from "./SearchBar.module.css";

const SearchBar = ({ handleSearchChange }) => {
  return (
    <div className={styles.search_bar}>
      <SearchIcon />
      <input
        className={styles.input}
        placeholder="Filter by Player Name"
        onChange={handleSearchChange}
      />
    </div>
  );
};

export default SearchBar;
