#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <cstdint>
#include <chrono>
#include <string>
#include <memory>
#include <thread>

namespace users
{
    #define MAXUSERS 1000
    class users{
    private:
        struct user{
            std::string userName;
            int32_t userID = -1;
            int32_t coins = 0;
            bool validation;
            std::chrono::time_point<std::chrono::system_clock> validationTime;
            std::string userPublicID;

        } typedef user;
       // std::vector<user> userContainer;
        std::map<std::string, user> userContainer;
        std::vector<std::string> publicIDs;
        int32_t userCount = 0;
        std::string serverName;

    public:
        users(int32_t userCount, std::string serverName){

        }
        bool addNewAdmin(){
            return true;
        }
        bool addNewUser(std::string userName, int32_t coins, bool validation){
            user newUser;
            newUser.userName = userName;
            newUser.userID = userCount;
            newUser.coins = coins;
            if(validation){
                newUser.validation = true;
                newUser.validationTime = std::chrono::system_clock::now();
                newUser.userPublicID = generateID(userName, userCount, newUser.validationTime);
                userContainer[newUser.userPublicID] = newUser;
            }
            else{
              //  newUser.validation = false;
               // userContainer.push_back(newUser);
            }
            std::cout << "User " << userName << " is added! The publicID: " << newUser.userPublicID << std::endl;
            publicIDs.push_back(newUser.userPublicID);
          //  std::this_thread::sleep_for(std::chrono::seconds(1));
            return validation;
        }
        std::string generateID(std::string userName, int32_t userID, std::chrono::time_point<std::chrono::system_clock> time){
            // Generating an hash for the user
            int32_t duration = time.time_since_epoch() / std::chrono::milliseconds(1);
            int64_t hash = 0;
            std::string userPublicID;
            for(int i = 0; i < userName.length(); i++){ 
                int32_t currentCharacter = userName[i];
                currentCharacter *= duration % (duration % 3333 + i*i);
                hash += currentCharacter << duration % (i + 1);
                duration /= 3;
            }

            for(int i = 0; i < 20; i++){
                int8_t hexValue = hash % 15 ;
                hash >>= 1;
                if (hexValue >= 10){
                    hexValue = 'A' + hexValue % 10;
                }
                else{
                    hexValue = '0' + hexValue;
                }
                userPublicID.push_back(hexValue);
            }
            while(userPublicID.length() < 20){
                userPublicID.push_back('0');
            }
            return userPublicID;

        }
        bool checkUser(std::string userPublicID){
            if(userContainer[userPublicID].userID != -1){
                std::cout << userPublicID << " is found!\nUser Name: "
                << userContainer[userPublicID].userName << "\nAvailable Coins: "
                << userContainer[userPublicID].coins << "\nValidation Time: "
                << userContainer[userPublicID].validationTime.time_since_epoch() / std::chrono::minutes(1) << "\n"<< std::endl;
                return true;
            }
            else{
                std::cout << "There is no user with the given public ID!\n" << std::endl;
                return false;
            }
        }
        std::string getPublicUserID(int32_t userID){
            return publicIDs.at(userID);
        }
        bool removeUser(std::string userPublicID){
            return true;
        }
    };

}
