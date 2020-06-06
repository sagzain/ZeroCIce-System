module TrawlNet
{
    interface Server {
        void execute(string message);
    };

    interface Intermediate { 
        void execute(string message);
    };
};