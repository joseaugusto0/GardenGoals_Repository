import { ChatTeardrop, ChatTeardropDots } from "phosphor-react";

interface HeaderProps{
    name?: string
}

function Header(props: HeaderProps){
    return (
        <div className="bg-secondary-500 h-16 w-full flex flex-wrap items-center align-middle justify-between ">
            <div className="flex absolute right-2">
                <button className="bg-violet-500 rounded mr-2">Hello, {props.name} </button>
                <ChatTeardropDots className="w-10 h-10 mr-2"></ChatTeardropDots>
            </div>
        </div>
    )
}

export default Header;