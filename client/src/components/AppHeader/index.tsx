import BrandLogo from "./components/BrandLogo";
import ConnectionStatus from "./components/ConnectionStatus";
import BluetoothButton from "./components/BluetoothButton";
import HeaderActions from "./components/HeaderActions";

export default function AppHeader() {
  return (
    <header className="bg-base-200 border-b border-base-300">
      <div className="max-w-6xl mx-auto gap-6 px-6 py-4 flex items-center justify-between">
        <BrandLogo />
        <div className="flex items-center gap-2">
          <ConnectionStatus />
          <BluetoothButton />
          <HeaderActions />
        </div>
      </div>
    </header>
  );
}
